from __future__ import unicode_literals
from collections import Iterable

try:
    from django.utils.six import PY3, string_types
except ImportError:
    # Django < 1.5. No Python 3 support
    PY3 = False
    string_types = basestring


def _flatten(iterable):
    """
    Given an iterable with nested iterables, generate a flat iterable
    """
    for i in iterable:
        if isinstance(i, Iterable) and not isinstance(i, string_types):
            for sub_i in _flatten(i):
                yield sub_i
        else:
            yield i


def get_variables(context):
    """
    Given a template context, return a sorted list of variable names in that
    context
    """
    variables = set(_flatten(
        (dicts.keys() for dicts in context.dicts)
    ))
    # Don't show the rendering tree 'block' as a variable in the context
    try:
        variables.remove('block')
    except KeyError:
        pass
    return sorted(list(variables))
