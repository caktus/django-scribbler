Release History
====================================

Release and change history for django-scribbler

v1.1.0 (Release 2021-12-20)
------------------------------------

- Add support for Django 3.2 through 4.0 (Thanks Petr Dlouhý)


v1.0.0 (Release 2019-10-28)
------------------------------------

- Add support for Django 2.0 through 2.2 (Thanks Petr Dlouhý)
- Drop support for Django < 2
- Drop support for Python 2

v0.9.0 (Release 2017-12-11)
------------------------------------

- Add support for Django 1.11 and Python 3.6
- Drop support for Django 1.9 and Python 3.2-3.3.
- Resulting support: Django 1.8, 1.10, or 1.11, and Python 2.7 or >= 3.4
- Fix how styles are loaded in the example project.

v0.8.0 (Release 2016-12-14)
------------------------------------

- Add support for Django 1.10, Python 3.5
- Improvements to docs
- Fix: Disallow scribble previews if the user does not have permission.
- Updated example project (including removing Twitter Bootstrap from it)


v0.7.0 (Released 2016-01-18)
------------------------------------

The release removed the use of RequireJS for bundling the required assets
and instead uses Browserify to create single required JS file. Updating
from a previous version requires changing how the JS file is included.

.. code-block:: html

    <script data-main="{% static 'scribbler/js/scribbler-min' %}" src="{% static 'scribbler/libs/require.js' %}"></script>

should be updated to

.. code-block:: html

    <script src="{% static 'scribbler/js/scribbler-min.js' %}"></script>


Features
_________________

- Added support for Django 1.9
- Added support for full screen edits
- Updated to CodeMirror 5.10
- Updated to Backbone 1.2.3, Underscore 1.8.3, jQuery 2.2.0

Backwards Incompatible Changes
__________________________________

- The update to jQuery 2.2 drops support for IE < 9
- The refactor to use browserify has dropped support for front-end plugins
- Dropped support for Django<=1.7, Python2.6, and Python3.2 (#101)
- South migrations have been removed since Django 1.6 support was removed


v0.6.0 (Released 2015-10-07)
------------------------------------

This release fixes some lingering issues with Django 1.8 support and integrates
Wheel support and features from the latest versions of Tox.

Features
_________________

- Added Wheel support (#96)
- Updated Tox and Travis to work with Tox 2.0+ (#90)
- Changed button color on editor
- Confirmed Python 3.4 support

Bug Fixes
_________________

- Fixed issues with Django 1.8 compatibility (#84)


v0.5.3 (Released 2014-06-13)
------------------------------------

- Fixed issues with Python 3 compatibility
- Fixed issues with Django 1.7+ compatibility
- Fixed issues with IE 8 compatibility


v0.5.2 (Released 2013-05-02)
------------------------------------

- Fixed issue with scribbler styles overlapping/overriding site styles. See #73


v0.5.1 (Released 2013-03-03)
------------------------------------

- Bug fix release for broken packaging


v0.5.0 (Released 2013-03-03)
------------------------------------

This release includes a major refactor of the JS code and adds support for writing
client-side plugins for customizing the editor.

Features
_________________

- Upgraded to CodeMirror 3.02
- Additional build/development utilities and documentation
- Started including a minified and optimized version of scribbler.js for production usage
- CSS is now built to include the base CodeMirror CSS and does not need to be added to the template separately

Bug Fixes
_________________

- Fixed a bug where you could not follow an internal link in the scribble content. See #66

Backwards Incompatible Changes
__________________________________

The static dependencies (RequireJS, CodeMirror and jQuery) were originally included in the repository
but have been removed. These are still included in the final distribution. However, if you installing
django-scribbler directly from git these will no longer be available. See the :doc:`contributing guide </contributing>`
for more information on building/installing an unstable version.


v0.4.0 (Released 2013-01-01)
------------------------------------

The length of the slug field has been reduced to fix problems with the unique contraint
on MySQL. Upgrading requires running a migration::

    manage.py migrate scribbler

Features
_________________

- Top level menu to reveal all editable sections on the page
- i18n support and initial French translation thanks to Nicolas Ippolito
- Created Transifex group for translations
- Added optional parameter to scribble tag to support shared scribbles thanks to David Ray
- Added the ability to discard a saved draft

Bug Fixes
_________________

- Fixed bug with newly included jQuery overriding an existing version. See #53
- Fixed bug with unique index on MySQL thanks to David Ray. See #61

Backwards Incompatible Changes
__________________________________

- The fix for #61 reduced the length of the slug field from 255 characters to 64


v0.3.0 (Released 2012-10-26)
------------------------------------

Features
_________________

- Autocomplete for Django template tags and filters
- New scribble_field template tag to allow editing of fields in arbitrary models


v0.2.1 (Released 2012-10-12)
------------------------------------

Bug Fixes
_________________

- Preview was broken when scribble was saved due to unique constraint. See #34


v0.2.0 (Released 2012-10-12)
------------------------------------

The editor now saves drafts on the client side by default. Python 3 support is
added when using the lastest Django master. There is also some additional documentation.

A unique constraint was added and upgrading from v0.1 does require a migration::

    manage.py migrate scribbler

- Added experimental Python >= 3.2 support when using Django 1.5dev
- Caktus Consulting Group has taken over the primary development
- Added the ability to save as a draft on the client side
- Added an official contributing guide

Bug Fixes
_________________

- Added unique constraint for url/slug pair. South migration is included.


v0.1.1 (Released 2012-08-25)
------------------------------------

Minor bug fix release for some JS and CSS issues.

Bug Fixes
_________________

- Fixed issue with the content editor z-index allowing content in front when open
- Fixed issue where links within editable content could not be clicked by editors


v0.1.0 (Released 2012-07-28)
------------------------------------

- Initial public release.

Features
_________________

- Template tag for rendering content blocks
- CodeMirror editor integration
