"Create/edit forms for scribble content."
from __future__ import unicode_literals

import sys

from django import forms
from django.template import StringOrigin
from django.template.debug import DebugLexer, DebugParser
from django.views.debug import ExceptionReporter

from .models import Scribble


class ScribbleForm(forms.ModelForm):

    class Meta(object):
        model = Scribble
        widgets = {
            'name': forms.HiddenInput,
            'slug': forms.HiddenInput,
            'url': forms.HiddenInput,
        }

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
                raise forms.ValidationError('Invalid Django Template')
        return content
