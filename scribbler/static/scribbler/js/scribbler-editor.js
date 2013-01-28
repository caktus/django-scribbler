/*jslint browser: true, newcap: true */
/*global define*/

var gettext = gettext || function (text) { 'use strict'; return text; };

define(['jquery', 'codemirror', 'simplehint', 'htmlmode'], function ($, CodeMirror) {
    'use strict';

    $.noConflict(true);

    var ScribbleEditor = {
        visible: false,
        rendering: false,
        errorLine: null,
        valid: true,
        element: null,
        controls: {},
        current: {},
        editor: null,
        scribbles: null,
        needsSave: false,
        needsDraft: false,
        init: function () {
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
                    onChange: function (editor) {
                        ScribbleEditor.needsSave = true;
                        ScribbleEditor.controls.save.removeClass('inactive');
                        ScribbleEditor.needsDraft = true;
                        ScribbleEditor.controls.draft.removeClass('inactive');
                        ScribbleEditor.submitPreview();
                    },
                    extraKeys: {'Tab': 'autocomplete'}
                };
                CodeMirror.commands.autocomplete = function (editor) {
                    CodeMirror.simpleHint(editor, CodeMirror.djangoHint);
                };
                this.editor = CodeMirror(
                    document.getElementById("scribbleEditorContainer"),
                    options
                );
                this.editor.selector = "scribbleEditorContainer";
                // Bind editor to the scribbles
                this.scribbles.each(function (i, elem) {
                    // Bind event handlers for each scribble
                    $(elem).click(function (e) {
                        // Allow click to follow links inside of scribble content
                        if (e.target.nodeName !== 'A') {
                            ScribbleEditor.open($(this));
                        }
                    });
                });
            }
        },
        buildControls: function () {
            // Build control bar
            var footerControls = $('<div></div>').addClass('controls clearfix');
            // Close button
            this.controls.close = $('<a>' + gettext('Close') + '</a>')
                .attr({title: gettext('Close'), href: '#'})
                .addClass('close')
                .click(function (e) {
                    e.preventDefault();
                    ScribbleEditor.close();
                });
            // Save button
            this.controls.save = $('<a>' + gettext('Save') + '</a>')
                .attr({title: gettext('Save'), href: "#"})
                .addClass('btn save inactive').click(function (e) {
                    e.preventDefault();
                    ScribbleEditor.submitSave();
                });
            this.controls.draft = $('<a>' + gettext('Save as Draft') + '</a>')
                .attr({title: gettext('Save as Draft'), href: "#"})
                .addClass('btn draft inactive').click(function (e) {
                    e.preventDefault();
                    ScribbleEditor.createDraft();
                });
            this.controls.discard = $('<a>' + gettext('Discard Draft') + '</a>')
                .attr({title: gettext('Discard Draft'), href: "#"})
                .addClass('btn discard inactive').click(function (e) {
                    e.preventDefault();
                    ScribbleEditor.editor.setValue($('[name$=content]', ScribbleEditor.current.form).val());
                    ScribbleEditor.deleteDraft();
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
                this.controls.discard,
                this.controls.draft,
                this.controls.save
            );
            this.element.append(footerControls);
        },
        open: function (scribble) {
            if (this.visible) {
                this.close();
            }
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
                this.editor.setValue(gettext('You do not have permission to edit this content.'));
            }
            this.element.animate({height: '300px'}, 500, function () {ScribbleEditor.editor.focus(); });
            this.visible = true;
            //ScribbleMenu.close();
            // Start background draft saving
            var checkDraft = function () {
                if (ScribbleEditor.needsDraft) {
                    ScribbleEditor.createDraft();
                }
            };
            this.backgroundDraft = setInterval(checkDraft, 3000);
        },
        close: function () {
            this.current.preview.hide();
            this.current.content.show();
            this.current = {};
            this.editor.setValue('');
            this.element.animate({height: 0}, 500);
            this.visible = false;
            if (this.backgroundDraft) {
                clearInterval(this.backgroundDraft);
            }
        },
        submitPreview: function (force) {
            if (this.current.form && (force || (!this.rendering && !this.editor.getOption('readOnly')))) {
                this.rendering = true;
                // Submit the form and display the preview
                $.post(
                    this.current.form.attr('action'),
                    this.getFormData(),
                    function (response) {
                        if (response.valid) {
                            CodeMirror.update_variables(response.variables);
                        }
                        ScribbleEditor.renderPreview(response);
                    },
                    'json'
                ).error(function (jqXHR, textStatus, errorThrown) {
                    var msg = 'Server response was "' + errorThrown + '"';
                    ScribbleEditor.setError(msg);
                }).complete(function () {
                    ScribbleEditor.rendering = false;
                });
            }
        },
        renderPreview: function (response) {
            if (this.errorLine !== null) {
                this.editor.setLineClass(this.errorLine, null, null);
            }
            this.controls.errors.html('');
            this.valid = response.valid;
            if (response.valid) {
                this.current.preview.html(response.html);
                this.current.preview.show();
                this.current.content.hide();
                this.controls.save.removeClass('inactive');
            } else {
                this.setError(response.error.message, response.error.line - 1);
            }
        },
        setError: function (msg, line) {
            if (typeof line !== 'undefined' && line !== null) {
                this.errorLine = line;
                this.editor.setLineClass(this.errorLine, null, "activeline");
            }
            this.controls.errors.html('<strong>' + gettext('Error:') + '</strong> ' + msg);
            this.valid = false;
            this.controls.save.addClass('inactive');
        },
        getFormData: function () {
            var result = {},
                prefix = '';
            if (this.current.form) {
                prefix = this.current.form.data('prefix');
                $(':input', this.current.form).each(function (i, input) {
                    var inputName = $(input).attr('name').replace(prefix + '-', ''),
                        inputValue = $(input).val();
                    if (inputName === 'content') {
                        result[inputName] = ScribbleEditor.editor.getValue();
                    } else {
                        result[inputName] = inputValue;
                    }
                });
            }
            return result;
        },
        submitSave: function () {
            if (this.current.form && this.valid) {
                // Submit the form and change current content
                $.post(
                    this.current.form.data('save'),
                    this.getFormData(),
                    function (response) {
                        ScribbleEditor.renderSave(response);
                    },
                    'json'
                ).error(function (jqXHR, textStatus, errorThrown) {
                    var msg = gettext('Server response was') + '"' + errorThrown + '"';
                    ScribbleEditor.setError(msg);
                });
            }
        },
        renderSave: function (response) {
            if (response.valid) {
                this.deleteDraft();
                this.needsSave = false;
                this.controls.save.addClass('inactive');
                this.current.form.data('save', response.url);
                this.current.content.html(this.current.preview.html());
                $('[name$=content]', this.current.form).val(this.editor.getValue());
                this.close();
            } else {
                this.setError(response.error.message);
            }
        },
        createDraft: function () {
            var scribble = null,
                path = window.location.pathname,
                slug = '';
            if (this.current.form) {
                // Check for localstorage and fallback to cookie
                scribble = this.editor.getValue();
                slug = this.current.form.data('prefix');
                if (typeof localStorage !== 'undefined' && localStorage !== null) {
                    localStorage[path + slug] = scribble;
                } else {
                    document.cookie = encodeURIComponent(slug) + '=' + encodeURIComponent(scribble) + ';' + 'path=' + path;
                }
                this.needsDraft = false;
                this.controls.draft.addClass('inactive');
                this.controls.discard.removeClass('inactive');
                this.setStatus(gettext('Draft saved...'));
            }
        },
        restoreDraft: function () {
            var scribble = null,
                path = window.location.pathname,
                slug = '',
                i,
                key,
                value,
                cookies = document.cookie.split(";"),
                cookieName;
            if (this.current.form) {
                // Check for localstorage and fallback to cookie
                slug = this.current.form.data('prefix');
                if (typeof localStorage !== 'undefined' && localStorage !== null) {
                    scribble = localStorage[path + slug];
                } else {
                    for (i = 0; i < cookies.length; i += 1) {
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
                    this.controls.discard.removeClass('inactive');
                    this.setStatus(gettext('Restored content from a draft...'));
                }
            }
        },
        deleteDraft: function () {
            var path = window.location.pathname,
                slug = '',
                yesterday = new Date();
            yesterday.setDate(yesterday.getDate() - 1);
            if (this.current.form) {
                // Check for localstorage and fallback to cookie
                slug = this.current.form.data('prefix');
                if (typeof localStorage !== 'undefined' && localStorage !== null) {
                    localStorage.removeItem(path + slug);
                } else {
                    document.cookie = encodeURIComponent(slug) + '=' + encodeURIComponent('') +
                        ';expires=' + yesterday.toUTCString() + ';path=' + path;
                }
                this.needsDraft = true;
                this.controls.draft.removeClass('inactive');
                this.controls.discard.addClass('inactive');
                this.setStatus(gettext('Restored original content...'));
            }
        },
        setStatus: function (msg) {
            // Append status message
            this.controls.status.fadeIn(500);
            this.controls.status.html(msg);
            // Callback to fade out the message
            setTimeout(function () {
                ScribbleEditor.controls.status.fadeOut(500, function () {
                    ScribbleEditor.controls.status.html("");
                });
            }, 2000);
        }
    };

    return ScribbleEditor; 
});
