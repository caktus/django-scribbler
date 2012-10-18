"Create/edit forms for scribble content."
from __future__ import unicode_literals

import sys

from django import forms
from django.db.models import ObjectDoesNotExist, FieldDoesNotExist
from django.template import StringOrigin
from django.template.debug import DebugLexer, DebugParser
from django.views.debug import ExceptionReporter
from django.core.urlresolvers import reverse

from .models import Scribble

class ScribbleFormMixin(object):

    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        if content:
            origin = StringOrigin(content)
            lexer = DebugLexer(content, origin)
            try:
                parser = DebugParser(lexer.tokenize())
                parser.parse()
            except Exception as e:
                self.exc_info = sys.exc_info()
                if not hasattr(self.exc_info[1], 'django_template_source'):
                    self.exc_info[1].django_template_source = origin, (0, 0)
                raise forms.ValidationError('Invalid Django Template')
        return content


class ScribbleForm(forms.ModelForm, ScribbleFormMixin):

    class Meta(object):
        model = Scribble
        widgets = {
            'name': forms.HiddenInput,
            'slug': forms.HiddenInput,
            'url': forms.HiddenInput,
        }

    def get_data_prefix(self):
        return self.instance.slug

    def get_save_url(self):
        return self.instance.get_save_url()

    def get_delete_url(self):
        return self.instance.get_delete_url()


class PreviewForm(ScribbleForm):

    def clean(self):
        "Override default clean to not check for slug/url uniqueness."
        return self.cleaned_data


class FieldScribbleForm(forms.Form, ScribbleFormMixin):
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, content_type, instance_pk, field_name, *args, **kwargs):
        field_value = kwargs.pop('field_value', None)
        if 'data' not in kwargs:
            kwargs['prefix'] = '{0}:{1}:{2}'.format(content_type.pk, instance_pk, field_name)
        super(FieldScribbleForm, self).__init__(*args, **kwargs)
        self.content_type = content_type
        self.instance_pk = instance_pk
        self.field_name = field_name
        self.fields['content'].initial = field_value
        try:
            self.fields['content'].required = not content_type.model_class()._meta.get_field_by_name(field_name)[0].blank
        except FieldDoesNotExist:
            # Error will be caught on form validation
            pass

    def clean(self):
        if not self.errors:
            ModelClass = self.content_type.model_class()
            try:
                current_instance = ModelClass.objects.get(pk=self.instance_pk)
            except ObjectDoesNotExist as e:
                raise forms.ValidationError(e)
            if not hasattr(current_instance, self.field_name):
                raise forms.ValidationError('{0} model has no field named {1}'.format(
                    ModelClass.__name__, self.field_name))
            setattr(current_instance, self.field_name, self.cleaned_data['content'])
            current_instance.full_clean()
        return self.cleaned_data

    def get_data_prefix(self):
        return self.prefix

    def get_save_url(self):
        args=(self.content_type.pk, self.instance_pk, self.field_name)
        return reverse('edit-scribble-field', args=args)

    def get_delete_url(self):
        raise NotImplemented()

    def save(self):
        self.content_type.model_class().objects.filter(pk=self.instance_pk).update(
            **{self.field_name: self.cleaned_data.get('content')})
