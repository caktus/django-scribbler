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

    var scribbles = $('.scribble-wrapper.with-controls');
    var open = false;
    
    if (scribbles.length > 0) {
        // Build editor footer
        var footer = $('<div id="scribbleEditorContainer"></div>');
        var footerControls = $('<div></div>').addClass('controls clearfix');
        var editor = null;
        // Footer controls
        var close = $('<a>Close</a>').attr({title: 'Close', href: '#'})
        .addClass('close').click(function(e) {
            e.preventDefault();
            var form = footer.data('form');
            var content = footer.data('content');
            var preview = footer.data('preview');
            preview.hide();
            content.show();
            $('[name$=content]', form).val(editor.getValue());
            footer.removeData(['content', 'preview', 'form']);
            footer.animate({height: 0}, 500);
        });
        var save = $('<a>Save</a>').attr({title: 'Save', href: "#"})
        .addClass('btn save').click(function(e) {
            e.preventDefault();
            var form = footer.data('form');
            var content = footer.data('content');
            var preview = footer.data('preview');
            function displayResults(response) {
                if (response.valid) {
                    form.data('save', response.url);
                    content.html(preview.html());
                    close.click();
                } else {
                    errors.html("<strong>Error:</strong> Content is not valid");
                }
            }
            var data = {};
            var prefix = form.data('prefix');
            $(':input', form).each(function(i, input) {
                var inputName = $(input).attr('name').replace(prefix + '-', '');
                var inputValue = $(input).val();
                if (inputName === 'content') {
                    data[inputName] = editor.getValue();
                } else {
                    data[inputName] = inputValue;
                }
            });
            // Submit the form and display the result
            $.post(form.data('save'), data, displayResults, 'json');
        });
        var del = $('<a>Delete</a>').attr({title: 'Delete', href: "#"})
        .addClass('btn delete').click(function(e) {
            e.preventDefault();
        });
        var errors = $('<span></span>').addClass('error-msg');
        footerControls.append(errors, close, save, del);
        footer.append(footerControls);

        $('body').append(footer);

        var currentChange = false;
        var lastError = null;
        var options = {
            mode: "text/html",
            tabMode: "indent",
            lineNumbers: true,
            onChange: function(editor) {
                if (!currentChange && !editor.getOption('readOnly')) {
                    currentChange = true;
                    var form = footer.data('form');
                    var content = footer.data('content');
                    var preview = footer.data('preview');
                    function renderPreview(response) {
                        if (lastError !== null) {
                            editor.setLineClass(lastError, null, null);
                        }
                        errors.html('');
                        if (response.valid) {
                            preview.html(response.html);
                            preview.show();
                            content.hide();
                            save.show();
                        } else {
                            lastError = response.error.line - 1;
                            editor.setLineClass(lastError, null, "activeline");
                            errors.html("<strong>Error:</strong> " + response.error.message);
                            save.hide();
                        }
                        currentChange = false;
                    }
                    var data = {};
                    var prefix = form.data('prefix');
                    $(':input', form).each(function(i, input) {
                        var inputName = $(input).attr('name').replace(prefix + '-', '');
                        var inputValue = $(input).val();
                        if (inputName === 'content') {
                            data[inputName] = editor.getValue();
                        } else {
                            data[inputName] = inputValue;
                        }
                    });
                    // Submit the form and display the preview
                    $.post(form.attr('action'), data, renderPreview, 'json');
                }
            }
        };
        editor = CodeMirror(
            document.getElementById("scribbleEditorContainer"),
            options
        );                
        
        scribbles.each(function(i, elem) {
            // Bind event handlers for each scribble
            var wrapper = $(elem);
            var content = $('.scribble-content.original', wrapper);
            var preview = $('.scribble-content.preview', wrapper);
            var form = $('.scribble-form', wrapper);
            var can_save = form.data('save');
            var can_delete = form.data('delete');

            wrapper.click(function(e) {
                e.preventDefault();
                footer.data('content', content);
                footer.data('preview', preview);
                footer.data('form', form);
                footer.show();
                footer.animate({height: '300px'}, 500);
                editor.focus();
                if (can_save) {
                    save.show();
                    editor.setOption('readOnly', false);
                    editor.setValue($('[name$=content]', form).val());
                } else {
                    save.hide();
                    editor.setOption('readOnly', true);
                    editor.setValue('You do not have permission to edit this content.');
                }
                if (can_delete) {
                    del.show();
                } else {
                    del.hide();
                }
            });
        });
    }
});
