/*
 * django-scribbler
 * Source: https://github.com/caktus/django-scribbler
 * Docs: http://django-scribbler.readthedocs.org/
 *
 * Copyright 2012, Caktus Consulting Group, LLC
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
        needsSave: false,
        needsDraft: false,
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
                    onChange: function(editor) {
                        ScribbleEditor.needsSave = true;
                        ScribbleEditor.controls.save.removeClass('inactive');
                        ScribbleEditor.needsDraft = true;
                        ScribbleEditor.controls.draft.removeClass('inactive');
                        ScribbleEditor.submitPreview();
                    }
                };
                this.editor = CodeMirror(
                    document.getElementById("scribbleEditorContainer"),
                    options
                );
                // Bind editor to the scribbles
                this.scribbles.each(function(i, elem) {
                    // Bind event handlers for each scribble
                    $(elem).click(function(e) {
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
            .addClass('btn save inactive').click(function(e) {
                e.preventDefault();
                ScribbleEditor.submitSave();
            });
            this.controls.draft = $('<a>Save as Draft</a>')
            .attr({title: 'Save as Draft', href: "#"})
            .addClass('btn draft inactive').click(function(e) {
                e.preventDefault();
                ScribbleEditor.createDraft();
            });
            // Error message
            this.controls.errors = $('<span></span>')
            .addClass('error-msg');
            // Status message
            this.controls.status = $('<span></span>')
            .addClass('status-msg');
            footerControls.append(
                this.controls.status,
                this.controls.errors,
                this.controls.close,
                this.controls.draft,
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
            if (this.current.can_save) {
                this.controls.save.show();
                this.editor.setOption('readOnly', false);
                this.editor.setValue($('[name$=content]', this.current.form).val());
                this.restoreDraft();
            } else {
                this.controls.save.hide();
                this.editor.setOption('readOnly', true);
                this.editor.setValue('You do not have permission to edit this content.');
            }
            this.element.animate({height: '300px'}, 500, function(){ScribbleEditor.editor.focus();});
            this.visible = true;
            // Start background draft saving
            var checkDraft = function() {
                if (ScribbleEditor.needsDraft) {
                    ScribbleEditor.createDraft();
                }
            };
            this.backgroundDraft = setInterval(checkDraft, 3000);
        },
        close: function() {
            this.current.preview.hide();
            this.current.content.show();
            $('[name$=content]', this.current.form).val(this.editor.getValue());
            this.current = {};
            this.editor.setValue('');
            this.element.animate({height: 0}, 500);
            this.visible = false;
            if (this.backgroundDraft) {
                clearInterval(this.backgroundDraft);
            }
        },
        submitPreview: function(force) {
            if (this.current.form && (force || (!this.rendering && !this.editor.getOption('readOnly')))) {
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
                this.controls.save.removeClass('inactive');
            } else {
                this.errorLine = response.error.line - 1;
                this.editor.setLineClass(this.errorLine, null, "activeline");
                this.controls.errors.html("<strong>Error:</strong> " + response.error.message);
                this.controls.save.addClass('inactive');
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
                this.deleteDraft();
                this.needsSave = false;
                this.controls.save.addClass('inactive');
                this.current.form.data('save', response.url);
                this.current.content.html(this.current.preview.html());
                this.close();
            } else {
                this.controls.errors.html("<strong>Error:</strong> Content is not valid");
            }
        },
        createDraft: function() {
            var scribble = null;
            var path = window.location.pathname;
            var slug = '';
            if (this.current.form) {
                // Check for localstorage and fallback to cookie
                scribble = this.editor.getValue();
                slug = this.current.form.data('prefix');
                if (typeof(localStorage) !== 'undefined' && localStorage !== null) {
                    localStorage[path + slug] = scribble;
                } else {
                    document.cookie = encodeURIComponent(slug) + '=' + encodeURIComponent(scribble) + ';' + 'path=' + path;
                }
                this.needsDraft = false;
                this.controls.draft.addClass('inactive');
                this.setStatus("Draft saved...");
            }
        },
        restoreDraft: function() {
            var scribble = null;
            var path = window.location.pathname;
            var slug = '';
            var i, key, value, cookies = document.cookie.split(";");
            if (this.current.form) {
                // Check for localstorage and fallback to cookie
                slug = this.current.form.data('prefix');
                if (typeof(localStorage) !== 'undefined' && localStorage !== null) {
                    scribble = localStorage[path + slug];
                } else {
                    for (i = 0; i < cookies.length; i++) {
                        key = cookies[i].substr(0, cookies[i].indexOf("="));
                        value = cookies[i].substr(cookies[i].indexOf("=") + 1);
                        key = decodeURIComponent(key.replace(/\+/g, " "));
                        if (key === cookieName) {
                            scribble = decodeURIComponent(value.replace(/\+/g, " "));
                            break;
                        }
                    }
                }
                if (scribble) {
                    this.editor.setValue(scribble);
                    this.submitPreview(true);
                    this.needsDraft = false;
                    this.controls.draft.addClass('inactive');
                    this.setStatus("Restored content from a draft...");
                }
            }
        },
        deleteDraft: function() {
            var path = window.location.pathname;
            var slug = '';
            var yesterday = new Date();
            yesterday.setDate(yesterday.getDate() -1);
            if (this.current.form) {
                // Check for localstorage and fallback to cookie
                slug = this.current.form.data('prefix');
                if (typeof(localStorage) !== 'undefined' && localStorage !== null) {
                    localStorage.removeItem(path + slug);
                } else {
                    document.cookie = encodeURIComponent(slug) + '=' + encodeURIComponent('') +
                    ';expires=' + yesterday.toUTCString() + ';path=' + path;
                }
                this.needsDraft = true;
                this.controls.draft.removeClass('inactive');
            }
        },
        setStatus: function(msg) {
            // Append status message
            this.controls.status.fadeIn(500);
            this.controls.status.html(msg);
            // Callback to fade out the message
            setTimeout(function() {
                ScribbleEditor.controls.status.fadeOut(500, function() {
                    ScribbleEditor.controls.status.html("");
                });
            }, 2000);
        }
    };

    $(document).ready(function(){ScribbleEditor.init();});
});
