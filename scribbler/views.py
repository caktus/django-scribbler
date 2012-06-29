from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.utils import simplejson as json
from django.views.debug import ExceptionReporter
from django.views.decorators.http import require_POST

from .forms import ScribbleForm


def build_scribble_context(scribble, request):
    "Create context for rendering a scribble or scribble preview."
    context = {
        'scribble': scribble,
    }
    return RequestContext(request, context)


@require_POST
def preview_scribble(request):
    "Render scribble content or return error information."
    results = {
        'valid': False,
        'html': '',
    }
    form = ScribbleForm(request.POST)
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
