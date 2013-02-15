/*global require, QUnit*/

require.config({
    baseUrl: "../../static/scribbler/js/",
    paths: {
        jquery: '../libs/jquery',
        codemirror: '../libs/codemirror/lib/codemirror',
        jsmode: '../libs/codemirror/mode/javascript/javascript',
        cssmode: '../libs/codemirror/mode/css/css',
        xmlmode: '../libs/codemirror/mode/xml/xml',
        htmlmode: '../libs/codemirror/mode/htmlmixed/htmlmixed',
        simplehint: '../libs/codemirror/addon/hint/simple-hint',
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

require(['menu-test.js', 'editor-test.js'], function () {
    //Tests loaded, run Tests
    QUnit.load();
    QUnit.start();
});