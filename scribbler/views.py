from __future__ import unicode_literals

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template import RequestContext, Template
from django.utils import simplejson as json
from django.views.debug import ExceptionReporter
from django.views.decorators.http import require_POST

from .forms import ScribbleForm, PreviewForm
from .models import Scribble


def build_scribble_context(scribble, request):
    "Create context for rendering a scribble or scribble preview."
    context = {
        'scribble': scribble,
    }
    return RequestContext(request, context)


@require_POST
def preview_scribble(request):
    "Render scribble content or return error information."
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    can_edit = request.user.has_perm('scribbler.change_scribble')
    can_create = request.user.has_perm('scribbler.add_scribble')
    if not (can_edit or can_create):
        return HttpResponseForbidden()
    results = {
        'valid': False,
        'html': '',
    }
    form = PreviewForm(request.POST)
    if form.is_valid():
        results['valid'] = True
        template = Template(form.cleaned_data.get('content', ''))
        context = build_scribble_context(form.instance, request)
        results['html'] = template.render(context)
    else:
        if hasattr(form, 'exc_info'):
            exc_type, exc_value, tb = form.exc_info
            reporter = ExceptionReporter(request, exc_type, exc_value, tb)
            reporter.get_template_exception_info()
            results['error'] = reporter.template_info
        else:
            # Not sure what to do here
            results['error'] = {
                'message': '',
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
        'id': None,
    }
    if form.is_valid():
        results['valid'] = True
        scribble = form.save()
        results['id'] = scribble.id
    results['url'] = scribble.get_save_url()
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
