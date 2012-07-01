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
        var save = $('<a>Save</a>').attr({title: 'Save', href: "#"}).addClass('btn save')
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
        footerControls.append(close, save);
        footer.append(footerControls);

        $('body').append(footer);

        var currentChange = false;
        var options = {
            mode: "text/html",
            tabMode: "indent",
            lineNumbers: true,
            onChange: function(editor) {
                if (!currentChange) {
                    currentChange = true;
                    var form = footer.data('form').find('form').eq(0);
                    var content = footer.data('content');
                    var preview = footer.data('preview');
                    function renderPreview(response) {
                        if (response.valid) {
                            preview.html(response.html);
                            preview.show();
                            content.hide();
                        } else {
                            console.log(response.error);
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
            //var controls = $('.scribble-controls', $(this));
            var content = $('.scribble-content.original', wrapper);
            var preview = $('.scribble-content.preview', wrapper);
            var form = $('.scribble-form', wrapper);

            wrapper.click(function(e) {
                e.preventDefault();
                footer.data('content', content);
                footer.data('preview', preview);
                footer.data('form', form);                
                editor.setValue($('[name$=content]', form).val());
                footer.show();
                footer.animate({height: '300px'}, 500);
                editor.focus();
            });
        });
    }
});
