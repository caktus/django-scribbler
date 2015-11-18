/*global require */

require('codemirror/addon/hint/show-hint');

var CodeMirror = require('codemirror');

function forEach(arr, f) {
    for (var i = 0, e = arr.length; i < e; ++i) {
        f(arr[i]);
    }
}

function arrayContains(arr, item) {
    if (!Array.prototype.indexOf) {
        var i = arr.length;
        while (i--) {
            if (arr[i] === item) {
                return true;
            }
        }
        return false;
    }
    return arr.indexOf(item) !== -1;
}

var TAG_RE = /\{\%\s?[^\s\%\}]*$/;
var VARIABLE_RE = /\{\{\s?[^\s\}\}]*$/;
var FILTER_RE = /\|[^\s\%\}]*$/;

var django_tags = ("autoescape block comment cycle debug extends filter " +
    "firstof for if ifchanged ifequal ifnotequal include load now regroup " +
    "spaceless ssi templatetag url widthratio").split(" ");

var django_filters = ("add addslashes capfirst center cut date default " +
    "default_if_none dictsort dictsortreversed divisibleby escape escapejs " +
    "filesizeformat first fix_ampersands floatformat force_escape get_digit " +
    "iriencode join last length length_is linebreaks linebreaksbr " +
    "linenumbers ljust lower make_list phone2numeric pluralize pprint " +
    "random removetags rjust safe slice slugify stringformat striptags time " +
    "timesince timeuntil title truncatewords truncatewords_html " +
    "unordered_list upper urlencode urlize urlizetrunc wordcount wordwrap " +
    "yesno").split(" ");

var django_variables = [];

function getCompletions(token, context, django_variables) {
    var found = [];
    var start = token.string;

    function maybeAdd(str) {
        if (str.indexOf(start) === 0 && !arrayContains(found, str)) {
            found.push(str);
        }
    }

    function gatherCompletions(token) {
        if (token.type === "tag") {
            forEach(django_tags, maybeAdd);
        } else if (token.type === "filter") {
            forEach(django_filters, maybeAdd);
        } else if (token.type === 'variable') {
            forEach(django_variables, maybeAdd);
        }
    }
    gatherCompletions(token);
    return found;
}

function scriptHint(editor, django_variables, getToken) {
    // Find the token at the cursor
    var cur = editor.getCursor(), token = getToken(editor, cur), tprop = token;
    token.type = 'unknown';
    token.closing = '';

    // Determine if the token is part of a tag, filter, or variable
    if (TAG_RE.test(token.string)) {
        token.type = 'tag';
        token.string = TAG_RE.exec(token.string)[0];
        token.closing = ' %}';
    }
    if (VARIABLE_RE.test(token.string)) {
        token.type = 'variable';
        token.string = VARIABLE_RE.exec(token.string)[0];
        token.closing = ' }}';
    }
    if (FILTER_RE.test(token.string)) {
        token.type = 'filter';
        token.string = FILTER_RE.exec(token.string)[0];
        token.closing = '';
    }
    token.string = token.string.replace(/[^\w]*/g, '');

    // Build list of found matches and return to autocompleter
    var found = getCompletions(token, [token], django_variables);
    return {
        token: token,
        list: found,
        from: {line: cur.line, ch: token.end - token.string.length},
        to: {line: cur.line, ch: token.end}
    };
}

CodeMirror.djangoHint = function (editor) {
    return scriptHint(editor, django_variables, function (e, cur) {
        return e.getTokenAt(cur);
    });
};
CodeMirror.update_variables = function (variables) {
    django_variables = variables;
};

return CodeMirror;
