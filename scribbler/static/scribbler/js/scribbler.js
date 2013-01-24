/*
 * django-scribbler
 * Source: https://github.com/caktus/django-scribbler
 * Docs: http://django-scribbler.readthedocs.org/
 *
 * Copyright 2012, Caktus Consulting Group, LLC
 * BSD License
 *
*/

/*jslint browser: true, newcap: true */
/*global require*/

var gettext = gettext || function (text) { 'use strict'; return text; };

require.config({
    paths: {
        jquery: '../libs/jquery.min',
        codemirror: '../libs/codemirror-compressed',
        simplehint: '../libs/simple-hint',
        scribblereditor: 'scribbler-editor',
        scribblermenu: 'scribbler-menu',
        djangohint: 'djangohint'
    },
    shim: {
        codemirror: {
            exports: 'CodeMirror'
        },
        simplehint: {
            exports: 'CodeMirror',
            deps: ['djangohint']
        },
        djangohint: {
            exports: 'CodeMirror',
            deps: ['codemirror']
        }
    }
});

require(['jquery', 'scribblereditor', 'scribblermenu', ], function ($, ScribbleEditor, ScribbleMenu) {
    'use strict';

    $(document).ready(function () {
        ScribbleEditor.init();
        ScribbleMenu.init();
    });
});
