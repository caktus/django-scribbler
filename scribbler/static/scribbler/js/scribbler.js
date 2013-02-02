/*
 * django-scribbler
 * Source: https://github.com/caktus/django-scribbler
 * Docs: http://django-scribbler.readthedocs.org/
 *
 * Copyright 2012-2013, Caktus Consulting Group, LLC
 * BSD License
 *
*/

/*global require*/

require.config({
    paths: {
        jquery: '../libs/jquery',
        codemirror: '../libs/codemirror/lib/codemirror',
        jsmode: '../libs/codemirror/mode/javascript/javascript',
        cssmode: '../libs/codemirror/mode/css/css',
        xmlmode: '../libs/codemirror/mode/xml/xml',
        htmlmode: '../libs/codemirror/mode/htmlmixed/htmlmixed',
        simplehint: '../libs/codemirror/lib/util/simple-hint',
        scribblereditor: 'scribbler-editor',
        scribblermenu: 'scribbler-menu',
        djangohint: 'djangohint',
        backbone: '../libs/backbone',
        underscore: '../libs/underscore'
    },
    shim: {
        codemirror: {
            exports: 'CodeMirror'
        },
        simplehint: {
            exports: 'CodeMirror',
            deps: ['codemirror']
        },
        jsmode: {
            exports: 'CodeMirror',
            deps: ['codemirror']
        },
        cssmode: {
            exports: 'CodeMirror',
            deps: ['codemirror']
        },
        xmlmode: {
            exports: 'CodeMirror',
            deps: ['codemirror']
        },
        htmlmode: {
            exports: 'CodeMirror',
            deps: ['xmlmode', 'jsmode', 'cssmode']
        },
        backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        underscore: {
            exports: '_'
        }
    }
});

require(['jquery', 'scribblereditor', 'scribblermenu'], function ($, ScribbleEditor, ScribbleMenu) {
    'use strict';

    $.noConflict(true);

    $(document).ready(function () {
        var editor = new ScribbleEditor(),
            menu = new ScribbleMenu();
        editor.render();
        editor.bind("open", menu.close, menu);
        menu.render();
    });
});
