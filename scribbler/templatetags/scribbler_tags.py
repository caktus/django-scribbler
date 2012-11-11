"Template tags for rendering snippet content."
from __future__ import unicode_literals

from django import template
from django.conf import settings
from django.core.cache import cache
from django.contrib.contenttypes.generic import ContentType
from django.core.exceptions import ImproperlyConfigured

from scribbler.conf import CACHE_TIMEOUT, CACHE_KEY_FUNCTION
from scribbler.forms import ScribbleForm, FieldScribbleForm
from scribbler.models import Scribble
from scribbler.views import build_scribble_context


register = template.Library()


class ScribbleNode(template.Node):
    "Render snippet or default block content."

    child_nodelists = ('nodelist_default', )

    def __init__(self, slug, nodelist, raw):
        self.slug = template.Variable(slug)
        self.nodelist_default = nodelist
        self.raw = raw

    def render(self, context):
        slug = self.slug.resolve(context)
        request = context.get('request', None)
        if request is None: # pragma: no cover
            if settings.DEBUG:
                msg = '"django.core.context_processors.request" is required to use django-scribbler'
                raise ImproperlyConfigured(msg)
            else:
                return ''
        url = request.path
        key = CACHE_KEY_FUNCTION(slug=slug, url=url)
        scribble = cache.get(key, None)
        if scribble is None:
            try:
                scribble = Scribble.objects.get(slug=slug, url=url)
            except Scribble.DoesNotExist:
                scribble = Scribble(slug=slug, url=url, content=self.raw)
            if CACHE_TIMEOUT:
                cache.set(key, scribble, CACHE_TIMEOUT)
        if scribble.pk:
            scribble_template = template.Template(scribble.content)
        else:
            scribble.content = self.raw
            scribble_template = self.nodelist_default
        scribble_context = build_scribble_context(scribble, request)
        content = scribble_template.render(scribble_context)
        wrapper_template = template.loader.get_template('scribbler/scribble-wrapper.html')
        context['scribble'] = scribble
        context['rendered_scribble'] = content
        user = context.get('user', None)
        show_controls = False
        can_edit = False
        can_add = False
        can_delete = False
        if user:
            can_edit = scribble.pk and user.has_perm('scribbler.change_scribble')
            can_add = (not scribble.pk) and user.has_perm('scribbler.add_scribble')
            can_delete = scribble.pk and user.has_perm('scribbler.delete_scribble')
        show_controls = can_edit or can_add or can_delete
        if can_edit or can_add:
            context['scribble_form'] = ScribbleForm(instance=scribble, prefix=slug)
        context['show_controls'] = show_controls
        context['can_add_scribble'] = can_add
        context['can_edit_scribble'] = can_edit
        context['can_delete_scribble'] = can_delete
        context['raw_content'] = self.raw
        return wrapper_template.render(context)


def rebuild_template_string(tokens):
    "Reconstruct the original template from a list of tokens."
    result = ''
    for token in tokens:
        value = token.contents
        if token.token_type == template.TOKEN_VAR:
            value = '{0} {1} {2}'.format(
                template.VARIABLE_TAG_START,
                value,
                template.VARIABLE_TAG_END,
            )
        elif token.token_type == template.TOKEN_BLOCK:
            value = '{0} {1} {2}'.format(
                template.BLOCK_TAG_START,
                value,
                template.BLOCK_TAG_END,
            )
        elif token.token_type == template.TOKEN_COMMENT:
            value = '{0} {1} {2}'.format(
                template.COMMENT_TAG_START,
                value,
                template.COMMENT_TAG_END,
            )
        result = '{0}{1}'.format(result, value)
    return result


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
        msg = "{0} tag requires exactly one argument.".format(*token.contents.split())
        raise template.TemplateSyntaxError(msg)
    # Save original token state
    tokens = parser.tokens[:]
    nodelist = parser.parse(('endscribble', ))
    # Remaining tokens are inside the block
    tokens = filter(lambda t: t not in parser.tokens, tokens)
    parser.delete_first_token()
    raw = rebuild_template_string(tokens)
    return ScribbleNode(slug=slug, nodelist=nodelist, raw=raw)


@register.simple_tag(takes_context=True)
def scribble_field(context, model_instance, field_name):
    """
    Renders a scribble-able field from a model instance.

    Usage:
    {% scribble_field model_instance 'field_name' %}
    """

    # TODO: This should maybe be a utility funciton
    request = context.get('request', None)
    if request is None: # pragma: no cover
        if settings.DEBUG:
            msg = '"django.core.context_processors.request" is required to use django-scribbler'
            raise ImproperlyConfigured(msg)
        else:
            return ''

    model_content_type = ContentType.objects.get_for_model(model_instance)
    field_value = getattr(model_instance, field_name)
    scribble_template = template.Template(field_value)
    scribble_context = build_scribble_context(None, request)
    rendered_content = scribble_template.render(scribble_context)
    context['rendered_scribble'] = rendered_content

    user = context.get('user', None)
    can_edit = False
    if user:
        perm_name = '{0}.change_{1}'.format(
            model_content_type.app_label,
            model_content_type.model,
        )
        can_edit = user.has_perm(perm_name)
    if can_edit:
        context['scribble_form'] = FieldScribbleForm(
            model_content_type, model_instance.pk, field_name, field_value=field_value)
    context['show_controls'] = can_edit
    context['can_add_scribble'] = False
    context['can_edit_scribble'] = can_edit
    context['can_delete_scribble'] = False
    context['raw_content'] = field_value
    wrapper_template = template.loader.get_template('scribbler/scribble-wrapper.html')
    return wrapper_template.render(context)

