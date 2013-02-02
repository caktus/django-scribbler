/*
 * django-scribbler
 * Source: https://github.com/caktus/django-scribbler
 * Docs: http://django-scribbler.readthedocs.org/
 *
 * Copyright 2012-2013, Caktus Consulting Group, LLC
 * BSD License
 *
*/

/*jslint browser: true, newcap: true */
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
        }
    }
});

require(['jquery', 'scribblereditor', 'scribblermenu'], function ($, ScribbleEditor, ScribbleMenu) {
    'use strict';

    $(document).ready(function () {
        ScribbleEditor.init();
        ScribbleMenu.init();
    });
});
