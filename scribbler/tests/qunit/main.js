/*global require, QUnit*/

require.config({
  baseUrl: "../../static/scribbler/js/",
  packages: [{
    name: 'codemirror',
    location: '../libs/codemirror',
    main: '/lib/codemirror'
  }],
  paths: {
      jquery: '../libs/jquery',
      scribblereditor: 'scribbler-editor',
      scribblermenu: 'scribbler-menu',
      djangohint: 'djangohint',
      backbone: '../libs/backbone',
      underscore: '../libs/underscore'
  },
  shim: {
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
