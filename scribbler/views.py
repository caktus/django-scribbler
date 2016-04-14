from __future__ import unicode_literals

import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template import RequestContext, Template
from django.views.debug import ExceptionReporter
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from .forms import ScribbleForm, PreviewForm, FieldScribbleForm
from .models import Scribble
from .utils import get_variables


def build_scribble_context(scribble):
    "Create context for rendering a scribble or scribble preview."
    context = {
        'scribble': scribble,
    }

    return context


@require_POST
def preview_scribble(request, ct_pk):
    "Render scribble content or return error information."
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    content_type = get_object_or_404(ContentType, pk=ct_pk)
    change_scribble = '{0}.change_{1}'.format(
        content_type.app_label, content_type.model)
    add_scribble = '{0}.add_{1}'.format(
        content_type.app_label, content_type.model)
    can_edit = request.user.has_perm(change_scribble)
    can_create = request.user.has_perm(add_scribble)
    if not (can_edit or can_create):
        return HttpResponseForbidden()
    results = {
        'valid': False,
        'html': '',
    }
    form = PreviewForm(request.POST)
    if form.is_valid():
        results['valid'] = True
        if hasattr(template, 'engines'):
            scribbler_template = template.engines['django'].from_string(form.cleaned_data.get('content', ''))
        else:
            scribbler_template = template.Template(form.cleaned_data.get('content', ''))
        context = build_scribble_context(form.instance)
        results['html'] = scribbler_template.render(context, request)
        results['variables'] = get_variables(RequestContext(request, context))
    else:
        if hasattr(form, 'exc_info'):
            # Pre Django 1.9
            try:
                exc_type, exc_value, tb = form.exc_info
                reporter = ExceptionReporter(request, exc_type, exc_value, tb)
                reporter.get_template_exception_info()
                results['error'] = reporter.template_info
            # Django >= 1.9: get_template_info() is moved from ExceptionReporter
            # onto Template. We pass the data it returns from scribbler/forms.py
            # to here.
            except (ValueError, AttributeError):
                # ValueError is raised when we pass in all 12 the arguments,
                # in form.exc_info and AttributeError is raised when
                # ExceptionReporter.get_template_exception_info() is called.
                results['error'] = form.exc_info
        else:
            # Not sure what to do here
            results['error'] = {
                'message': 'Content is not valid',
                'line': '',
            }
    content = json.dumps(results, cls=DjangoJSONEncoder, ensure_ascii=False)
    return HttpResponse(content, content_type='application/json')


@require_POST
def create_edit_scribble(request, scribble_id=None):
    "Create a new Scribble or edit an existing one."
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    if scribble_id is not None:
        scribble = get_object_or_404(Scribble, pk=scribble_id)
        if not request.user.has_perm('scribbler.change_scribble'):
            return HttpResponseForbidden()
    else:
        scribble = Scribble()
        if not request.user.has_perm('scribbler.add_scribble'):
            return HttpResponseForbidden()
    form = ScribbleForm(request.POST, instance=scribble)
    results = {
        'valid': False,
    }
    if form.is_valid():
        results['valid'] = True
        scribble = form.save()
    results['url'] = scribble.get_save_url()
    content = json.dumps(results, cls=DjangoJSONEncoder, ensure_ascii=False)
    return HttpResponse(content, content_type='application/json')


@require_POST
def edit_scribble_field(request, ct_pk, instance_pk, field_name):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    content_type = get_object_or_404(ContentType, pk=ct_pk)
    perm_name = '{0}.change_{1}'.format(content_type.app_label, content_type.model)
    if not request.user.has_perm(perm_name):
        return HttpResponseForbidden()
    form = FieldScribbleForm(content_type, instance_pk, field_name, data=request.POST)
    results = {
        'valid': False,
    }
    if form.is_valid():
        results['valid'] = True
        form.save()
    else:
        results['error'] = {
            'message': ','.join('%s' % e for e in form.errors.values()),
            'line': '',
        }
    results['url'] = form.get_save_url()
    content = json.dumps(results, cls=DjangoJSONEncoder, ensure_ascii=False)
    return HttpResponse(content, content_type='application/json')


@require_POST
def delete_scribble(request, scribble_id):
    "Delete an existing scribble."
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    scribble = get_object_or_404(Scribble, pk=scribble_id)
    if not request.user.has_perm('scribbler.delete_scribble'):
        return HttpResponseForbidden()
    scribble.delete()
    results = {
        'valid': True,
        'url': scribble.get_save_url()
    }
    content = json.dumps(results, cls=DjangoJSONEncoder, ensure_ascii=False)
    return HttpResponse(content, content_type='application/json')
