django-scribbler
===================

django-scribbler is an application for managing snippets of text for a Django website.
Similar projects include django-flatblocks, django-chunks and django-pagelets. This
project attempts to take some of the best concepts from those previous projects as
well as focus on giving the users instant feedback inspired by Bret Victor's
`Inventing on Principle <http://vimeo.com/36579366>`_ talk.

.. image::
    https://secure.travis-ci.org/caktus/django-scribbler.png?branch=master
    :alt: Build Status
        :target: https://secure.travis-ci.org/caktus/django-scribbler


Features
--------------------------------------

- Simple template tag for defining snippet blocks with default text
- Template tag for displaying and editing fields from arbitrary models
- Front-end editing of snippets with the powerful `CodeMirror <http://codemirror.net/>`_ editor
- Live in-place preview of content while editing
- The full power of the Django template language in the snippet blocks
- Experimental Python 3 support

A very simple demo site is available at http://scribbler-mlavin.dotcloud.com/ (username: demo password: demo) 


Installation
--------------------------------------

django-scribbler requires Django >= 1.3 and Python >= 2.6. Starting with version v0.2
there will be experimental Python 3 support (3.2+). Using Python 3 requires using
the in-development version of Django (1.5dev).

To install from PyPi::
    
    pip install django-scribbler


Documentation
-----------------------------------

Documentation on using django-scribbler is available on 
`Read The Docs <http://readthedocs.org/docs/django-scribbler/>`_.


License
--------------------------------------

django-scribbler is released under the BSD License. See the 
`LICENSE <https://github.com/caktus/django-scribbler/blob/master/LICENSE>`_ file for more details.


Contributing
--------------------------------------

If you think you've found a bug or are interested in contributing to this project
check out `django-scribbler on Github <https://github.com/caktus/django-scribbler>`_. A
full contributing guide can be found in the `online documentation <http://django-scribbler.readthedocs.org/en/latest/contributing.html>`_.

If you are interested in translating django-scribbler into your native language
you can join the `Transifex project <https://www.transifex.com/projects/p/django-scribbler/>`_.

Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services>`_.

