/*global require, QUnit*/
var menuTest = require('./menu-test.js');
var editorTest = require('./editor-test.js');
    //Tests loaded, run Tests
    QUnit.load();
    QUnit.start();
    menuTest();
    editorTest();
