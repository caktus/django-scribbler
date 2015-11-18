/*
 * django-scribbler
 * Source: https://github.com/caktus/django-scribbler
 * Docs: http://django-scribbler.readthedocs.org/
 *
 * Copyright 2012-2014, Caktus Consulting Group, LLC
 * BSD License
 *
*/

/*global require */
var $ = require('jquery');
var _ = require('underscore');
var ScribbleMenu = require('./scribbler-menu.js');
var ScribbleEditor = require('./scribbler-editor.js');

var pluginlist = [],
    script;

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
