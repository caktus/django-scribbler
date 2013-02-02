Release History
====================================

Release and change history for django-scribbler


v0.5.0 (Not Yet Released)
------------------------------------


Features
_________________

- Upgraded to CodeMirror 2.38
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
