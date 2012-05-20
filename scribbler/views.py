from django.template import RequestContext


def build_scribble_context(scribble, request):
    "Create context for rendering a scribble or scribble preview."
    context = {
        'scribble': scribble,
    }
    return RequestContext(request, context)
