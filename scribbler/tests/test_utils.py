"Tests for utility functions."
from contextlib import contextmanager

from django.test import TestCase
from django.template import RequestContext, Template
from django.test.client import RequestFactory

from .test_views import BaseViewTestCase

from scribbler.utils import _flatten, get_variables


@contextmanager
def context_context_manager(context):
    # bind_template added in Django 1.8
    if hasattr(context, 'bind_template'):
        template = Template('')
        with context.bind_template(template):
            yield
    else:
        yield


class FlattenTestCase(TestCase):
    """TestCase for _flatten"""

    def test_flattens_inner_list(self):
        "Assure arbitrarily nested lists are flattened"
        nested_list = [1, [2, [3, 4, [5], ], 6, 7], 8]
        self.assertEqual(list(_flatten(nested_list)), list(range(1, 9)))

    def test_flattens_tuples(self):
        "Assure nested tuples are also flattened"
        nested_tuples = (1, (2, 3, (4, ), 5), 6)
        self.assertEqual(list(_flatten(nested_tuples)), list(range(1, 7)))

    def test_flattens_sets(self):
        "Assure nested sets are flattened"
        nested_sets = set([1, frozenset([2, 3]), 4])
        self.assertEqual(list(_flatten(nested_sets)), list(range(1, 5)))

    def test_flatten_nested_combinations(self):
        "Assure nested iterables are flattened"
        nested = [1, frozenset([2, 3]), (4, (5,), 6), [7], 8]
        self.assertEqual(list(_flatten(nested)), list(range(1, 9)))

    def test_flatten_generator(self):
        "Assure generators are flattened"
        gens = [1, list(range(2, 4)), (num for num in (4, list(range(5, 7))))]
        self.assertEqual(list(_flatten(gens)), list(range(1, 7)))

    def test_flatten_string_unchanged(self):
        "Assure strings are left intact"
        data = ['abc', ['abc', ['abc']], 'abc']
        self.assertEqual(list(_flatten(data)), ['abc', 'abc', 'abc', 'abc'])


def test_processor(request):
    return {
        'custom_processor_var': 1,
    }


class GetVariablesTestCase(BaseViewTestCase):
    """TestCase for get_variables"""

    def setUp(self):
        factory = RequestFactory()
        self.request = factory.get('/foo/')
        self.known_globals = ['csrf_token', 'request', 'user']

    def _get_context(self, dict_=None, processors=None):
        return RequestContext(self.request, dict_, processors=processors)

    def test_global_context_processors(self):
        """
        Assure get_variables contains known global context processors such as
        request and user
        """
        context = self._get_context()
        with context_context_manager(context):
            variables = set(get_variables(context))
            self.assertTrue(variables.issuperset(set(self.known_globals)))

    def test_returned_variable(self):
        """Assure get_variables returns variables unique to the context."""
        context = self._get_context({})
        with context_context_manager(context):
            variables = get_variables(context)
            self.assertTrue('a' not in variables)

        context = self._get_context({'a': 3})
        with context_context_manager(context):
            variables = get_variables(context)
            self.assertTrue('a' in variables)

    def test_custom_processors(self):
        context = self._get_context({}, processors=[])
        with context_context_manager(context):
            variables = get_variables(context)
            self.assertTrue('custom_processor_var' not in variables)
        context = self._get_context({}, processors=[test_processor])
        with context_context_manager(context):
            variables = get_variables(context)
            self.assertTrue('custom_processor_var' in variables)
