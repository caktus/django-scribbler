from collections import Iterable


def _flatten(iterable):
    """
    Given an iterable with nested iterables, generate a flat iterable
    """
    for i in iterable:
        if isinstance(i, Iterable) and not isinstance(i, str):
            for sub_i in _flatten(i):
                yield sub_i
        else:
            yield i


def get_variables(context):
    """
    Given a template context, return a sorted list of variable names in that
    context
    """
    variables = set(context.flatten().keys())
    # Don't show the rendering tree 'block' as a variable in the context
    try:
        variables.remove('block')
    except KeyError:
        pass
    return sorted(list(variables))
