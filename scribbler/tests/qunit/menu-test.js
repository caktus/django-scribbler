/*global define, module, test, expect, equal, ok*/

define(['jquery', 'underscore', 'scribblermenu'], function ($, _, ScribbleMenu) {
    var menu,
        scribbleTemplate = _.template($("#scribble-template").html());

    module("Menu Tests", {
        setup: function () {
            // Add a scribble to the fixture area
            $('#qunit-fixture').append(scribbleTemplate({}));
            menu = new ScribbleMenu();
            menu.render();
        },
        teardown: function () {
            menu.destroy();
        }
    });

    test("Menu Render", function () {
        expect(2);
        equal($("#scribbleMenuContainer").length, 1, "Menu was not added.");
        ok(!menu.visible, "Menu should not be visible.");
    });

    test("Menu Open", function () {
        expect(1);
        menu.open();
        ok(menu.visible, "Menu should be visible.");
    });

    test("Menu Close", function () {
        expect(1);
        menu.open();
        menu.close();
        ok(!menu.visible, "Menu should not be visible.");
    });

    test("Menu Highlight", function () {
        expect(2);
        var highlighted = $('.scribble-wrapper.highlight', '#qunit-fixture');
        equal(highlighted.length, 0, "Scribble should not be highlighted.");
        menu.highlight();
        highlighted = $('.scribble-wrapper.highlight', '#qunit-fixture');
        equal(highlighted.length, 1, "Scribble should be highlighted.");
    });
});