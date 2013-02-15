/*global define*/

define(["require", "jquery", "underscore"], function (require, $, _) {
    var themes = [
        'default', 'ambiance', 'blackboard', 'cobalt', 'eclipse', 'elegant',
        'erlang-dark', 'lesser-dark', 'monokai', 'neat', 'night', 'rubyblue',
        'solarized light', 'solarized dark', 'twilight', 'vibrant-ink', 'xq-dark'
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
                    cssName = selected.split(" ")[0],
                    cssUrl = require.toUrl("./../../libs/codemirror/theme/" + cssName + ".css"),
                    id = "#code-mirror-theme-" + cssName,
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