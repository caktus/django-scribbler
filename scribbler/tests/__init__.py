from django.db import models

class DaysLog(models.Model):
    happenings = models.CharField(max_length=44, default="Default Text", unique=True)

from .test_templatetags import RenderScribbleTestCase, RenderScribbleFieldTestCase
from .test_views import PreviewTestCase, CreateTestCase, EditTestCase, DeleteTestCase, EditFieldTestCase
from .test_utils import FlattenTestCase, GetVariablesTestCase
