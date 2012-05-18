"Template tags for rendering snippet content."

from django import template

from scribbler.models import Scribble


register = template.Library()


class ScribbleNode(template.Node):
    "Render snippet or default block content."
    
    child_nodelists = ('nodelist_default', )

    def __init__(self, slug, nodelist):
        self.slug = template.Variable(slug)
        self.nodelist_default = nodelist

    def render(self, context):
        slug = self.slug.resolve(context)
        request = context.get('request', None)
        scribble = None
        if request:
            try:
                scribble = Scribble.objects.get(slug=slug, url=request.path)
            except Scribble.DoesNotExist:
                scribble = None
        if scribble:
            nodelist = Template(scribble.content)
        else:
            nodelist = self.nodelist_default
        return nodelist.render(context)


@register.tag
def scribble(parser, token):
    """
    Renders a scribble by slug. First looks for a scribble matching the
    current url and slug then looks for shared scribbles by slug.

    Usage:
    {% scribble 'sidebar' %}
        <p>This is the default.</p>
    {% endscribble %}
    """
    try:
        tag_name, slug = token.split_contents()
    except ValueError:
        msg = u"{0} tag requires exactly one argument.".format(*token.contents.split())
        raise template.TemplateSyntaxError(msg)
    nodelist = parser.parse(('endscribble', ))
    parser.delete_first_token()
    return ScribbleNode(slug=slug, nodelist=nodelist)
