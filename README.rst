django-scribbler
===================

django-scribbler is an application for managing snippets of text for a Django website.
Similar projects include django-flatblocks, django-chunks and django-pagelets. This
project attempts to take some of the best concepts from those previous projects as
well as focus on giving the users instant feedback inspired by Bret Victor's
`Inventing on Principle <http://vimeo.com/36579366>`_ talk.

.. image::
    https://secure.travis-ci.org/mlavin/django-scribbler.png?branch=master
    :alt: Build Status
        :target: https://secure.travis-ci.org/mlavin/django-scribbler


Features
--------------------------------------

- Simple template tag for defining snippet blocks with default text
- Front-end editing of snippets with the powerful `CodeMirror <http://codemirror.net/>`_ editor
- Live in-place preview of content while editing
- The full power of the Django template language in the snippet blocks


Installation
--------------------------------------

django-scribbler requires Django >= 1.3 and Python >= 2.6 (but < 3.0)

To install from PyPi::
    
    pip install django-scribbler


Documentation
-----------------------------------

Documentation on using django-scribbler is available on 
`Read The Docs <http://readthedocs.org/docs/django-scribbler/>`_.


Contributing
--------------------------------------

If you think you've found a bug or are interested in contributing to this project
check out `django-scribbler on Github <https://github.com/mlavin/django-scribbler>`_.

