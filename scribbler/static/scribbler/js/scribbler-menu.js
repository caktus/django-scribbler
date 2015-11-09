/*global require, module */

var $ = require('jquery');
var Backbone = require('backbone');
var _ = require('underscore');
Backbone.$ = $;


var gettext = gettext || function (text) {
    'use strict';
    return text;
};

var ScribbleMenu = Backbone.View.extend({
    id: 'scribbleMenuContainer',
    tagName: 'div',
    initialize: function () {
        this.visible = false;
        this.controls = {};
        this.scribbles = $('.scribble-wrapper.with-controls');
    },
    events: {
        'click .tab': 'toggle',
        'click .control-panel .reveal': 'highlight'
    },
    render: function () {
        if (this.scribbles.length > 0) {
            this.buildControls();
            this.$el.css('top', -1000);
            $('body').append(this.$el);
            this.close();
        }
    },
    buildControls: function () {
        // Build control bar
        this.menuControls = $('<div></div>').addClass('control-panel');
        // Open/Close button
        this.controls.tab = $('<a><span class="hot-dog"></span><span class="hot-dog"></span><span class="hot-dog"></span></a>')
            .attr({title: gettext('Toggle Menu')})
            .addClass('tab');
        // Reveal button
        this.controls.reveal = $('<a>' + gettext('Show all scribbles') + '</a>')
            .attr({title: gettext('Show all scribbles')})
            .addClass('reveal');
        this.menuControls.append(this.controls.reveal);
        this.$el.append(this.menuControls);
        this.$el.append(this.controls.tab);
    },
    open: function (scribble) {
        this.$el.animate({top: 0}, 150);
        this.visible = true;
    },
    close: function () {
        var height = this.menuControls.height();
        this.$el.animate({top: -1 * (5 + height)}, 200);
        this.visible = false;
        this.scribbles.removeClass('highlight');
    },
    toggle: function () {
        if (this.visible) {
            this.close();
        } else {
            this.open();
        }
    },
    highlight: function () {
        this.scribbles.addClass('highlight');
    },
    destroy: function () {
        this.undelegateEvents();
        this.remove();
    }
});

module.exports = ScribbleMenu;
