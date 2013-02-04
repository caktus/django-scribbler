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


Editor API
------------------------------------


Menu API
------------------------------------


Enabling the Plugin
------------------------------------