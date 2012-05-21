"Create/edit forms for scribble content."

from django import forms

from .models import Scribble


class ScribbleForm(forms.ModelForm):

    class Meta(object):
        model = Scribble
        widgets = {
            'name': forms.HiddenInput,
            'slug': forms.HiddenInput,
            'url': forms.HiddenInput,
        }
