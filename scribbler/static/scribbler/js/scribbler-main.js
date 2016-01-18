/*
 * django-scribbler
 * Source: https://github.com/caktus/django-scribbler
 * Docs: http://django-scribbler.readthedocs.org/
 *
 * Copyright 2012-2016, Caktus Consulting Group, LLC
 * BSD License
 *
*/

/*global require */
var $ = require('jquery');
var _ = require('underscore');
var ScribbleMenu = require('./scribbler-menu.js');
var ScribbleEditor = require('./scribbler-editor.js');

$(document).ready(function () {
    var editor = new ScribbleEditor(),
        menu = new ScribbleMenu();
    editor.bind("open", menu.close, menu);
    editor.render();
    menu.render();
});
