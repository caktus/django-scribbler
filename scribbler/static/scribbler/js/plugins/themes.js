/*global define*/

define(["require", "jquery", "underscore"], function (require, $, _) {
    var themes = [
        'default', 'ambiance', 'blackboard', 'cobalt', 'eclipse', 'elegant',
        'erlang-dark', 'lesser-dark', 'monokai', 'neat', 'night', 'rubyblue',
        'vibrant-ink', 'xq-dark'
    ];
    // Theme switcher plugin
    function plugin(editor, menu) {
        // Select input will all available themes
        var control = $("<select>")
            .addClass("theme")
            .css("float", "right")
            .css("margin", "10px")
            .on("change", function (e) {
                var selected = $(this).val(),
                    cssUrl = require.toUrl("./../../libs/codemirror/theme/" + selected + ".css"),
                    id = "#code-mirror-theme-" + selected,
                    stylesheet = $("link" + id);
                if (stylesheet.length === 0 && selected !== "default") {
                    // Inject the theme CSS
                    stylesheet = $("<link>", {"type": "text/css", "rel": "stylesheet", "href": cssUrl, "id": id});
                    $("head").append(stylesheet);
                }
                editor.editor.setOption("theme", selected);
            });
        _.each(themes, function (theme) {
            control.append($("<option>").text(theme));
        });
        menu.menuControls.append(control);
    }
    return plugin;
});