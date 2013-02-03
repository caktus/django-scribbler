/*global define, module, test, expect, equal, ok*/

define(['jquery', 'underscore', 'scribblereditor'], function ($, _, ScribbleEditor) {
    var scribbleTemplate = _.template($("#scribble-template").html());

    module("Editor Tests", {
        setup: function () {
            // Patch AJAX requests
            this.xhr = sinon.useFakeXMLHttpRequest();
            var requests = this.requests = [];

            this.xhr.onCreate = function (xhr) {
                requests.push(xhr);
            };
            // Add a scribble to the fixture area
            $('#qunit-fixture').append(scribbleTemplate({}));
            this.scribble = $('.scribble-wrapper', '#qunit-fixture').eq(0);
            this.editor = new ScribbleEditor();
            this.editor.render();
        },
        teardown: function () {
            this.editor.destroy();
            this.xhr.restore();
        }
    });

    test("Editor Render", function () {
        expect(2);
        equal($("#scribbleEditorContainer").length, 1, "Editor was not added.");
        ok(!this.editor.visible, "Editor should not be visible.");
    });

    test("Editor Open", function () {
        var content = $('#id_header-content', this.scribble).val();
        expect(2);
        editor.open(scribble);
        ok(this.editor.visible, "Editor should be visible.");
        equal(this.editor.editor.getValue(), content, "Editor should have scribble content.");
    });
});