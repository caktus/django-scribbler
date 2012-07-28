/*
 * django-scribbler
 * Source: https://github.com/mlavin/django-scribbler
 * Docs: http://django-scribbler.readthedocs.org/
 *
 * Copyright 2012, Mark Lavin
 * BSD License
 *
*/

require.config({
    paths: {
        jquery: 'https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min',
        codemirror: '../libs/codemirror-compressed'
    },
    shim: {
        codemirror: {
            exports: 'CodeMirror'
        }
    }
});

require(['jquery', 'codemirror'], function($, CodeMirror) {
    var ScribbleEditor = {
        visible: false,
        rendering: false,
        errorLine: null,
        element: null,
        controls: {},
        current: {},
        editor: null,
        scribbles: null,
        init: function() {
            this.scribbles = $('.scribble-wrapper.with-controls');
            if (this.scribbles.length > 0) {
                this.element = $('<div id="scribbleEditorContainer"></div>');
                this.buildControls();
                $('body').append(this.element);
                // Initialize CodeMirror editor
                var options = {
                    mode: "text/html",
                    tabMode: "indent",
                    lineNumbers: true,
                    onChange: function(editor) {ScribbleEditor.submitPreview();}
                };
                this.editor = CodeMirror(
                    document.getElementById("scribbleEditorContainer"),
                    options
                );
                // Bind editor to the scribbles
                this.scribbles.each(function(i, elem) {
                    // Bind event handlers for each scribble
                    $(elem).click(function(e) {
                        e.preventDefault();
                        ScribbleEditor.open($(this));
                    });
                });
            }
        },
        buildControls: function() {
            // Build control bar
            var footerControls = $('<div></div>').addClass('controls clearfix');
            // Close button
            this.controls.close = $('<a>Close</a>')
            .attr({title: 'Close', href: '#'})
            .addClass('close')
            .click(function(e) {
                e.preventDefault();
                ScribbleEditor.close();
            });
            // Save button
            this.controls.save = $('<a>Save</a>')
            .attr({title: 'Save', href: "#"})
            .addClass('btn save').click(function(e) {
                e.preventDefault();
                ScribbleEditor.submitSave();
            });
            // Error message
            this.controls.errors = $('<span></span>')
            .addClass('error-msg');
            footerControls.append(
                this.controls.errors,
                this.controls.close,
                this.controls.save
            );
            this.element.append(footerControls);
        },
        open: function(scribble) {
            this.current.content = $('.scribble-content.original', scribble);
            this.current.preview = $('.scribble-content.preview', scribble);
            this.current.form = $('.scribble-form', scribble);
            this.current.can_save = this.current.form.data('save');
            this.current.can_delete = this.current.form.data('delete');
            this.element.show();
            this.element.animate({height: '300px'}, 500);   
            if (this.current.can_save) {
                this.controls.save.show();
                this.editor.setOption('readOnly', false);
                this.editor.setValue($('[name$=content]', this.current.form).val());
            } else {
                this.controls.save.hide();
                this.editor.setOption('readOnly', true);
                this.editor.setValue('You do not have permission to edit this content.');
            }
            this.editor.focus();
            this.visible = true;
        },
        close: function() {
            this.current.preview.hide();
            this.current.content.show();
            $('[name$=content]', this.current.form).val(this.editor.getValue());
            this.current = {};
            this.editor.setValue('');
            this.element.animate({height: 0}, 500);
            this.visible = false;
        },
        submitPreview: function() {
            if (this.current.form && !this.rendering && !this.editor.getOption('readOnly')) {
                this.rendering = true;
                // Submit the form and display the preview
                $.post(
                    this.current.form.attr('action'),
                    this.getFormData(), 
                    function(response) {
                        ScribbleEditor.renderPreview(response);
                    },
                    'json'
                );
            }
        },
        renderPreview: function(response) {
            if (this.errorLine !== null) {
                this.editor.setLineClass(this.errorLine, null, null);
            }
            this.controls.errors.html('');
            if (response.valid) {
                this.current.preview.html(response.html);
                this.current.preview.show();
                this.current.content.hide();
                this.controls.save.show();
            } else {
                this.errorLine = response.error.line - 1;
                this.editor.setLineClass(this.errorLine, null, "activeline");
                this.controls.errors.html("<strong>Error:</strong> " + response.error.message);
                this.controls.save.hide();
            }
            this.rendering = false;
        },
        getFormData: function() {
            var result = {};
            var prefix = '';
            if (this.current.form) {
                prefix = this.current.form.data('prefix');
                $(':input', this.current.form).each(function(i, input) {
                    var inputName = $(input).attr('name').replace(prefix + '-', '');
                    var inputValue = $(input).val();
                    if (inputName === 'content') {
                        result[inputName] = ScribbleEditor.editor.getValue();
                    } else {
                        result[inputName] = inputValue;
                    }
                });
            }
            return result;
        },
        submitSave: function() {
            if (this.current.form && !this.errorLine) {
                // Submit the form and change current content
                $.post(
                    this.current.form.data('save'),
                    this.getFormData(),
                    function(response) {
                        ScribbleEditor.renderSave(response);
                    },
                    'json'
                );
            }
        },
        renderSave: function(response) {
            if (response.valid) {
                this.current.form.data('save', response.url);
                this.current.content.html(this.current.preview.html());
                this.close();
            } else {
                this.controls.errors.html("<strong>Error:</strong> Content is not valid");
            }
        }
    };

    $(document).ready(function(){ScribbleEditor.init();});
});
