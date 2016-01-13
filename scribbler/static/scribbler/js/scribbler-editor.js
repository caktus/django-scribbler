/*global require, module */

require('codemirror/mode/xml/xml');
require('codemirror/mode/javascript/javascript');
require('codemirror/mode/css/css');
require('codemirror/mode/htmlmixed/htmlmixed');
require('codemirror/addon/display/fullscreen');
require('./djangohint');

var $ = require('jquery');
var Backbone = require('backbone');
var _ = require('underscore');
Backbone.$ = $;
var CodeMirror = require('codemirror');

var gettext = gettext || function (text) {
    'use strict';
    return text;
};

var ScribbleEditor = Backbone.View.extend({
    id: 'scribbleEditorContainer',
    tagName: 'div',
    initialize: function () {
        var self = this;
        this.visible = false;
        this.rendering = false;
        this.errorLine = null;
        this.controls = {};
        this.current = {};
        this.needsSave = false;
        this.needsDraft = false;
        this.scribbles = $('.scribble-wrapper.with-controls');
        this.editorOptions =  {
                mode: "text/html",
                tabMode: "indent",
                lineNumbers: true,
                extraKeys: {
                  "F11": function(cm) {
                    cm.setOption("fullScreen", !cm.getOption("fullScreen"));
                    if ($('.CodeMirror-fullscreen').length) {
                      $('#scribbleEditorContainer').addClass("scribbleEditor-fullscreen");
                    }
                    else {
                      $('#scribbleEditorContainer').removeClass("scribbleEditor-fullscreen");
                    }
                  },
                  "Esc": function(cm) {
                    if (cm.getOption("fullScreen")) {
                        cm.setOption("fullScreen", false);
                    }
                    $('.scribbleEditor-fullscreen').removeClass("scribbleEditor-fullscreen");
                  },
                  'Tab': 'autocomplete'
                }
                };
        CodeMirror.commands.autocomplete = function (editor) {
            CodeMirror.showHint(editor, CodeMirror.djangoHint);
        };
    },
    events: {
        'click .controls .closed': 'close',
        'click .controls .save': 'submitSave',
        'click .controls .draft': 'createDraft',
        'click .controls .discard': 'deleteDraft'
    },
    render: function () {
        var self = this;
        if (this.scribbles.length > 0) {
            this.buildControls();
            $('body').append(this.$el);
            this.editor = new CodeMirror(document.getElementById(this.id), this.editorOptions);
            this.editor.on("change", function (editor, change) {
                self.needsSave = true;
                self.controls.save.removeClass('inactive');
                self.needsDraft = true;
                self.controls.draft.removeClass('inactive');
                self.submitPreview();
            });
            this.editor.selector = this.id;
            // Bind editor to the scribbles
            this.scribbles.each(function (i, elem) {
                // Bind event handlers for each scribble
                $(elem).click(function (e) {
                    // Allow click to follow links inside of scribble content
                    if (e.target.nodeName !== 'A') {
                        self.open($(this));
                    }
                });
            });
        }
    },
    buildControls: function () {
        // Build control bar
        var footerControls = $('<div></div>').addClass('controls');
        // Close button
        this.controls.close = $('<a>' + gettext('Close') + '</a>')
            .attr({title: gettext('Close')})
            .addClass('closed');
        // Save button
        this.controls.save = $('<a>' + gettext('Save') + '</a>')
            .attr({title: gettext('Save')})
            .addClass('save inactive');
        this.controls.draft = $('<a>' + gettext('Save Draft') + '</a>')
            .attr({title: gettext('Save as Draft')})
            .addClass('draft inactive');
        this.controls.discard = $('<a>' + gettext('Discard') + '</a>')
            .attr({title: gettext('Discard Draft')})
            .addClass('discard inactive');
        // Error message
        this.controls.errors = $('<span></span>')
            .addClass('error-msg');
        // Status message
        this.controls.status = $('<span></span>')
            .addClass('status-msg');
        // Fullscreen instructions
        this.controls.fullscreen = $('<div>' + gettext('Press ') +
            '<strong>' + gettext('F11') + '</strong>' +
            gettext(' to enter/exit Fullscreen edit') + '</div>')
            .addClass('fullscreen');
        footerControls.append(
            this.controls.status,
            this.controls.errors,
            this.controls.close,
            this.controls.discard,
            this.controls.draft,
            this.controls.save,
            this.controls.fullscreen
        );
        this.$el.append(footerControls);
    },
    open: function (scribble) {
        var self = this;
        if (this.visible) {
            this.close();
        }
        this.current.content = $('.scribble-content.original', scribble);
        this.current.preview = $('.scribble-content.preview', scribble);
        this.current.form = $('.scribble-form', scribble);
        this.current.can_save = this.current.form.data('save');
        this.current.can_delete = this.current.form.data('delete');
        this.$el.show();
        this.trigger('open');
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
        this.$el.animate({height: '300px'}, 500, function () {self.editor.focus(); });
        this.visible = true;
        // Start background draft saving
        var checkDraft = function () {
            if (self.needsDraft) {
                self.createDraft();
            }
        };
        this.backgroundDraft = setInterval(checkDraft, 3000);
    },
    close: function () {
        this.current.preview.hide();
        this.current.content.show();
        this.current = {};
        this.editor.setValue('');
        this.$el.animate({height: 0}, 500);
        this.visible = false;
        if (this.backgroundDraft) {
            clearInterval(this.backgroundDraft);
        }
        $('#scribbleEditorContainer').removeClass("scribbleEditor-fullscreen");
        $('.CodeMirror.cm-s-default').removeClass("CodeMirror-fullscreen").css("height", "");
        this.trigger('close');
    },
    submitPreview: function (force) {
        var self = this;
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
                    self.renderPreview(response);
                },
                'json'
            ).error(function (jqXHR, textStatus, errorThrown) {
                var msg = 'Server response was "' + errorThrown + '"';
                self.setError(msg);
            }).complete(function () {
                self.rendering = false;
            });
        }
    },
    renderPreview: function (response) {
        var self = this;
        if (this.visible) {
            if (this.errorLine !== null) {
                this.editor.removeLineClass(this.errorLine, "background", "activeline");
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
        }
    },
    setError: function (msg, line) {
        if (typeof line !== 'undefined' && line !== null) {
            this.errorLine = line;
            this.editor.addLineClass(this.errorLine, "background", "activeline");
        }
        this.controls.errors.html('<strong>' + gettext('Error:') + '</strong> ' + msg);
        this.valid = false;
        this.controls.save.addClass('inactive');
    },
    getFormData: function () {
        var result = {},
            prefix = '',
            self = this;
        if (this.current.form) {
            prefix = this.current.form.data('prefix');
            $(':input', this.current.form).each(function (i, input) {
                var inputName = $(input).attr('name').replace(prefix + '-', ''),
                    inputValue = $(input).val();
                if (inputName === 'content') {
                    result[inputName] = self.editor.getValue();
                } else {
                    result[inputName] = inputValue;
                }
            });
        }
        return result;
    },
    submitSave: function () {
        var self = this;
        if (this.current.form && this.valid) {
            // Submit the form and change current content
            $.post(
                this.current.form.data('save'),
                this.getFormData(),
                function (response) {
                    self.renderSave(response);
                },
                'json'
            ).error(function (jqXHR, textStatus, errorThrown) {
                var msg = gettext('Server response was') + '"' + errorThrown + '"';
                self.setError(msg);
            });
        }
        $('#scribbleEditorContainer').removeClass("scribbleEditor-fullscreen");
        $('.CodeMirror.cm-s-default').removeClass("CodeMirror-fullscreen").css("height", "");
    },
    renderSave: function (response) {
        if (response.valid) {
            this.needsSave = false;
            this.controls.save.addClass('inactive');
            this.current.form.data('save', response.url);
            this.current.content.html(this.current.preview.html());
            $('[name$=content]', this.current.form).val(this.editor.getValue());
            this.deleteDraft();
            this.close();
        } else if (response.error) {
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
        this.editor.setValue($('[name$=content]', this.current.form).val());
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
        var self = this;
        // Append status message
        this.controls.status.fadeIn(500);
        this.controls.status.html(msg);
        // Callback to fade out the message
        setTimeout(function () {
            self.controls.status.fadeOut(500, function () {
                self.controls.status.html("");
            });
        }, 2000);
    },
    destroy: function () {
        this.undelegateEvents();
        this.remove();
    }
});

module.exports = ScribbleEditor;
