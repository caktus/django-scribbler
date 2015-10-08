/*
 * django-scribbler
 * Source: https://github.com/caktus/django-scribbler
 * Docs: http://django-scribbler.readthedocs.org/
 *
 * Copyright 2012-2014, Caktus Consulting Group, LLC
 * BSD License
 *
*/

/*global require*/

require.config({
    paths: {
        jquery: '../libs/jquery',
        scribblereditor: 'scribbler-editor',
        scribblermenu: 'scribbler-menu',
        djangohint: 'djangohint',
        backbone: '../libs/backbone',
        underscore: '../libs/underscore'
    },
    packages: [{
      name: 'codemirror',
      location: '../libs/codemirror',
      main: '/lib/codemirror'
    }]
});

require(['jquery', 'underscore', 'scribblereditor', 'scribblermenu'], function ($, _, ScribbleEditor, ScribbleMenu) {
    'use strict';

    var pluginlist = [],
        script;

    $.noConflict(true);

    // Dynamically loads additional plugins for django-scribbler
    function pluginLoader(name, editor, menu) {
        var path = "./plugins/" + name;
        require([path], function (plugin) {
            plugin.call(null, editor, menu);
        });
    }

    script = $("script[data-scribbler-plugins]");

    if (script.length) {
        pluginlist = script.data("scribblerPlugins").split(",");
    }

    $(document).ready(function () {
        var editor = new ScribbleEditor(),
            menu = new ScribbleMenu();
        editor.bind("open", menu.close, menu);
        function executePlugin(name) {
            pluginLoader(name, editor, menu);
        }
        _.map(pluginlist, executePlugin);
        editor.render();
        menu.render();
    });
});
