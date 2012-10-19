Using the Editor
====================================

django-scribbler makes use of `CodeMirror <http://codemirror.net/>`_ to create
a powerful client-side editor. We've added a couple features to make it easier
when working with Django templates.


Context Inspection
------------------------------------

When using the editor you can inspect the current context by starting a variable
node with ``{{ `` and hitting tab. As noted in the quick start introduction,
scribble content can be any valid Django template. The context provided when 
rendering the scribble includes anything added by the set of
``TEMPLATE_CONTEXT_PROCESSORS``. This would include ``STATIC_URL``, ``MEDIA_URL``,
``LANGUAGE_CODE``, the current ``user`` and others. Developers may choose to add
context processors to include additional content for rendering scribbles.
