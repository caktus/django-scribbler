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


Tempate Tag/Filter Completion
------------------------------------

Similar to how the editor can tab-complete the context variables, you can tab
complete template tags when ``{% `` has been opened. The built-in filters can
be tab-completed when the pipe ``|`` character is detected inside of a variable node.
Currently this will only complete the built-in tags and filter and will not include any
additional tags or filters which might be added by loading additional libaries inside the scribble.


Saving Drafts
------------------------------------

While editting the scribble content, the editor will periodically save the current
editor content as a draft. These drafts are saved on the client side using local storage
(if supported by the browser) or a cookie. While that means you won't be able to see
or use these drafts in another browser, it does mean that you work will not be lost
if there is a failure on the server will saving changes or making edits. When the editor
is opened it will restore any draft that is found.
