/*global define, module, test, expect, equal, ok*/
var $ = require('jquery');
var _ = require('underscore');
var ScribbleMenu = require('../../static/scribbler/js/scribbler-menu.js');
var template = require('./template.html');

module.exports = function() {
    var menu,
        scribbleTemplate = template.scribble_template({});

    QUnit.module("Menu Tests", {
        beforeEach: function () {
            // Add a scribble to the fixture area
            $('#qunit-fixture').append(scribbleTemplate);
            menu = new ScribbleMenu();
            menu.render();
        },
        afterEach: function () {
            menu.destroy();
        }
    });

    QUnit.test("Menu Render", function () {
        expect(2);
        equal($("#scribbleMenuContainer").length, 1, "Menu was not added.");
        ok(!menu.visible, "Menu should not be visible.");
    });

    QUnit.test("Menu Open", function () {
        expect(1);
        menu.open();
        ok(menu.visible, "Menu should be visible.");
    });

    QUnit.test("Menu Close", function () {
        expect(1);
        menu.open();
        menu.close();
        ok(!menu.visible, "Menu should not be visible.");
    });

    QUnit.test("Menu Highlight", function () {
        expect(2);
        var highlighted = $('.scribble-wrapper.highlight', '#qunit-fixture');
        equal(highlighted.length, 0, "Scribble should not be highlighted.");
        menu.highlight();
        highlighted = $('.scribble-wrapper.highlight', '#qunit-fixture');
        equal(highlighted.length, 1, "Scribble should be highlighted.");
    });
}
