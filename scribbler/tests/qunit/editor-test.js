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
        this.editor.open(this.scribble);
        ok(this.editor.visible, "Editor should be visible.");
        equal(this.editor.editor.getValue(), content, "Editor should have scribble content.");
    });

    test("Editor Close", function () {
        expect(2);
        this.editor.open(this.scribble);
        this.editor.close();
        ok(!this.editor.visible, "Editor should not be visible.");
        equal(this.editor.editor.getValue(), '', "Editor should be empty.");
    });

    test("Editor Submit Preview", function () {
        expect(2);
        this.editor.open(this.scribble);
        this.editor.rendering = false;
        this.requests.length = 0;
        this.editor.submitPreview();
        equal(this.requests.length, 1, "Request submitted for preview.");
        equal(this.requests[0].url, '/scribble/preview/');
    });

    test("Editor Currently Rendering", function () {
        expect(1);
        this.editor.open(this.scribble);
        this.editor.rendering = true;
        this.requests.length = 0;
        this.editor.submitPreview();
        equal(this.requests.length, 0, "No preview should be submitted.");
    });

    test("Editor Force Preview", function () {
        expect(2);
        this.editor.open(this.scribble);
        this.editor.rendering = true;
        this.requests.length = 0;
        this.editor.submitPreview(true);
        equal(this.requests.length, 1, "Force the preview submission.");
        equal(this.requests[0].url, '/scribble/preview/');
    });

    test("Editor Preview Success", function () {
        var preview = $('.preview', this.scribble);
        expect(1);
        this.editor.open(this.scribble);
        this.editor.rendering = false;
        this.requests.length = 0;
        this.editor.submitPreview();
        this.requests[0].respond(200, {"Content-Type": "application/json"},
             '{"valid": true, "html": "Foo", "variables": []}'
        );
        equal(preview.html(), 'Foo', "Preview div should be updated.");
    });

    test("Editor Preview Error", function () {
        var preview = $('.preview', this.scribble);
        var original = preview.html();
        expect(2);
        this.editor.open(this.scribble);
        this.editor.rendering = false;
        this.requests.length = 0;
        this.editor.submitPreview();
        this.requests[0].respond(200, {"Content-Type": "application/json"},
            '{"valid": false, "html": "", "error": {"message": "Bar", "line": 1}}'
        );
        equal(preview.html(), original, "Preview div should be unchanged.");
        equal(this.editor.controls.errors.text(), "Error: Bar", "Error message should be set.");
    });

    test("Editor Save", function () {
        expect(2);
        this.editor.open(this.scribble);
        this.editor.valid = true;
        this.requests.length = 0;
        this.editor.submitSave();
        equal(this.requests.length, 1, "Request submitted for save.");
        equal(this.requests[0].url, '/scribble/edit/1/');
    });

    test("Editor Invalid Save", function () {
        expect(1);
        this.editor.open(this.scribble);
        this.editor.valid = false;
        this.requests.length = 0;
        this.editor.submitSave();
        equal(this.requests.length, 0, "No save should be submitted.");
    });

    test("Editor Save Success", function () {
        var current = $('.original', this.scribble);
        $('.preview', this.scribble).html("Foo");
        expect(2);
        this.editor.open(this.scribble);
        this.editor.valid = true;
        this.requests.length = 0;
        this.editor.submitSave();
        this.requests[0].respond(200, {"Content-Type": "application/json"},
             '{"valid": true, "url": "/scribble/edit/1/"}'
        );
        equal(current.html(), 'Foo', "Current div will be copied from preview.");
        ok(!this.editor.visible, "Editor should be closed.");
    });

    test("Editor Save Error", function () {
        var current = $('.original', this.scribble);
        var original = current.html();
        expect(2);
        this.editor.open(this.scribble);
        this.editor.valid = true;
        this.requests.length = 0;
        this.editor.submitSave();
        this.requests[0].respond(200, {"Content-Type": "application/json"},
             '{"valid": false, "url": "/scribble/edit/1/"}'
        );
        equal(current.html(), original, "Current div should be unchanged.");
        ok(this.editor.visible, "Editor should still be open.");
    });
});