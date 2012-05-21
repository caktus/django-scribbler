/*
 * django-scribbler
 * Source: https://github.com/mlavin/django-scribbler
 * Docs: http://django-scribbler.readthedocs.org/
 *
 * Copyright 2012, Mark Lavin
 * BSD License
 *
*/

$(document).ready(function() {

    $('.scribble-wrapper.with-controls').each(function(i, elem) {
        // Bind event handlers for each scribble
        var wrapper = $(elem);
        var controls = $('.scribble-controls', $(this));
        var content = $('.scribble-content.original', wrapper);
        var preview = $('.scribble-content.preview', wrapper);
        var form = $('.scribble-form', wrapper);

        wrapper.hover(function() {
            controls.show('fast');
        }, function() {
            if (!wrapper.hasClass('active')) {
                controls.hide('fast');
            }
        });

        $('.edit', controls).click(function(e) {
            e.preventDefault();
            wrapper.addClass('active');
            content.hide();
            preview.hide();
            form.show('fast');
            var editor = form.data('editor');
            if (!editor) {
                editor = CodeMirror.fromTextArea(
                    document.getElementById("id_content"),
                    {mode: "text/html", tabMode: "indent", lineNumbers: true}
                );
                form.data('editor', editor);
            } 
        });

        $('.cancel', controls).click(function(e) {
            e.preventDefault();
            wrapper.removeClass('active');
            form.hide();
            preview.hide();
            content.show('fast');
        });

    });
});
