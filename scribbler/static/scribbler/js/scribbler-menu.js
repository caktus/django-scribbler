/*jslint browser: true, newcap: true */
/*global define*/

var gettext = gettext || function (text) { 'use strict'; return text; };

define(['jquery'], function ($) {
    'use strict';

    $.noConflict(true);

    var ScribbleMenu = {
        visible: false,
        controls: {},
        scribbles: null,
        init: function () {
            this.scribbles = $('.scribble-wrapper.with-controls');
            if (this.scribbles.length > 0) {
                this.element = $('<div id="scribbleMenuContainer"></div>');
                this.buildControls();
                this.element.css('top', -1000);
                $('body').append(this.element);
                this.close();
            }
        },
        buildControls: function () {
            // Build control bar
            this.menuControls = $('<div></div>').addClass('control-panel');
            // Open/Close button
            this.controls.tab = $('<a><span class="hot-dog"></span><span class="hot-dog"></span><span class="hot-dog"></span></a>')
                .attr({title: gettext('Toggle Menu'), href: '#'})
                .addClass('tab')
                .click(function (e) {
                    e.preventDefault();
                    if (ScribbleMenu.visible) {
                        ScribbleMenu.close();
                    } else {
                        ScribbleMenu.open();
                    }
                });
            // Reveal button
            this.controls.reveal = $('<a>' + gettext('Show all scribbles') + '</a>')
                .attr({title: gettext('Show all scribbles'), href: "#"})
                .addClass('reveal').click(function (e) {
                    e.preventDefault();
                    ScribbleMenu.scribbles.addClass('highlight');
                });
            this.menuControls.append(this.controls.reveal);
            this.element.append(this.menuControls);
            this.element.append(this.controls.tab);
        },
        open: function (scribble) {
            this.element.animate({top: 0}, 150);
            this.visible = true;
        },
        close: function () {
            var height = this.menuControls.height();
            this.element.animate({top: -1 * (5 + height)}, 200);
            this.visible = false;
            this.scribbles.removeClass('highlight');
        }
    };

    return ScribbleMenu;
});
