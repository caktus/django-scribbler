PLUGINS CURRENTLY BROKEN
====================================
It is possible that plugins may be added back in the future, but as of right now there is
no working plugin feature.  All following documentation only pertains to versions 0.6.0 
and earlier.


Writing Editor Plugins
====================================

django-scribbler editor has some nice features like a live preview, auto-saving
drafts and tab completion of template tags and template context. If you find yourself
wanting to extend the functionality of the editor or top menu you can write a
plugin.


Basic Setup
------------------------------------

Client-side plugins to be added to a ``scribbler/js/plugins`` folder inside of
static files folder. If you are writing this plugin for a reusable application
then it would live inside of the app's ``static`` folder. The plugin name
will be the name of the .js file. For example we might create a ``demo`` plugin
by adding a ``scribbler/js/plugins/demo.js`` inside of our app ``static`` folder.


Writing the Plugin
------------------------------------

django-scribbler uses `RequireJS <http://requirejs.org/>`_ to load its Javascript
requirements. Since this code is loaded in a closure, plugins need to be
written in the `AMD <http://requirejs.org/docs/whyamd.html#amd>`_ format. The
basic format is::

    define(function () {
        function plugin(editor, menu) {
            // Plugin code goes here...
        }
        return plugin;
    });

This has an advantage in that the plugin code can declare requirements as well as
take advantage of existing modules used by the scribbler code. For instance if your
plugin requires jQuery you can define the requirement::

    define(['jquery'], function ($) {
        function plugin(editor, menu) {
            // Plugin code goes here...
        }
        return plugin;
    });

The plugin code itself should return a function which takes two arguments: ``editor``
and ``menu``. Each are the current instance of the editor and the menu respectively.
Within the plugin you can add additional controls or event bindings. The APIs for
both the editor and the menu are given below.

.. note::

    The plugins are executed after the editor and menu have been initialized but they
    are loaded asynchronously. That means the editor and menu may be fully rendered
    before the plugins are executed.


Enabling the Plugin
------------------------------------

Plugins are enable by listing them in a ``data-scribbler-plugins`` attribute on the
script tag::

    <script data-scribbler-plugins="themes"
        data-main="{{ STATIC_URL }}scribbler/js/scribbler{% if not debug %}-min{% endif %}"
        src="{{ STATIC_URL }}scribbler/libs/require.js"></script>

If mutliple plugins used then they should be comma seperated as in
``data-scribbler-plugins="themes,other"``.

.. note::

    Since the plugins are loaded asynchronously they might not load in the same order
    they are listed. Plugins should be written and designed with that limitation in mind.


Available Libraries
------------------------------------

As noted above you can use the ``define`` call to load additional dependencies/libraries
for your plugin from the set of libraries used by django-scribbler. The available libraries
are:

- require: `RequireJS 2.1.4 <http://requirejs.org/>`_
- jquery: `jQuery 1.8.3 <http://jquery.com/>`_
- codemirror: `CodeMirror 2.38 <http://codemirror.net/>`_
- underscore: `Underscore 1.4.4 <http://documentcloud.github.com/underscore/>`_
- backbone: `Backbone 0.9.10 <http://backbonejs.org/>`_


Editor API
------------------------------------

The ``editor`` passed in the plugin is an instance of the ``ScribbleEditor`` defined
in ``scribbler/js/scribbler-editor.js``. Below is a list of some of the most relevant
functions and properties for controlling the editor.

.. js:attribute:: editor.scribbles

    This is a jQuery object containing all of the scribble divs available on the page
    for editting.

.. js:attribute:: editor.footerControls

    A jQuery object for the div wrapping all of the editor button controls (Save,
    Save Draft, Discard Draft, Close). If you want to add additional controls they
    should be appended here.

.. js:attribute:: editor.editor

    ``editor.editor`` is the instance of the CodeMirror editor. You can manipulate this
    object to change the options with ``editor.editor.setOption``. See the CodeMirror
    usage manual for available options: http://codemirror.net/doc/manual.html

.. js:function:: editor.open(scribble)

    Opens the editor to edit the given scribble.

.. js:function:: editor.close()

    Closes the editor.

.. js:function:: editor.submitPreview(force)

    Submits the current editor content to render the live preview. By default this
    will not submit if the editor is currently in the process of rendering a preview.
    Passing ``true`` into the call will force the submission.

.. js:function:: editor.submitSave()

    Submits the editor content to save the current scribble content. By default
    the save will not be submitted if the last preview was not valid.

.. js:function:: editor.getFormData()

    Prepares the current form data for preview/save submission. If you want to
    pass additional data to the server your plugin could extend this function.

.. js:function:: editor.createDraft()

    Saves the current editor content as a local draft.

.. js:function:: editor.restoreDraft()

    Restores the editor content from the last saved draft if available.

.. js:function:: editor.deleteDraft()

    Discards last saved draft.

.. js:function:: editor.setStatus(msg)

    Displays a status message to the user in the header of the editor.

.. js:function:: editor.destroy()

    Removes the editor from the DOM and unbinds all event handling.


Menu API
------------------------------------

The ``menu`` passed in the plugin is an instance of the ``ScribbleMenu`` defined
in ``scribbler/js/scribbler-menu.js``. Below is a list of some of the most relevant
functions and properties for controlling the menu.

.. js:attribute:: menu.scribbles

    This is a jQuery object containing all of the scribble divs available on the page
    for editing.

.. js:attribute:: menu.menuControls

    A jQuery object for the div wrapping all of the menu button controls.
    If you want to add additional controls they should be appended here.

.. js:function:: menu.open()

    Opens the top menu bar.

.. js:function:: menu.close()

    Closes the top menu bar.

.. js:function:: menu.toggle()

    Toggles the open/close state of the top menu bar.

.. js:function:: menu.highlight()

    Highlights all editable scribble areas on the page.

.. js:function:: menu.destroy()

    Removes the menu from the DOM and unbinds all event handling.
