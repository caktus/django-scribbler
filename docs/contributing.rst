Contributing Guide
====================================

There are a number of ways to contribute to django-scribbler. If you are interested
in making django-scribbler better then this guide will help you find a way to contribute.


Ways to Contribute
------------------------------------

You can contribute to the project by submitting bug reports, feature requests 
or documentation updates through the Github `issues <https://github.com/caktus/django-scribbler/issues>`_.


Getting the Source
------------------------------------

You can clone the repository from Github::

    git clone git://github.com/caktus/django-scribbler.git

However this checkout will be read only. If you want to contribute code you should
create a fork and clone your fork. You can then add the main repository as a remote::

    git clone git@github.com:<your-username>/django-scribbler.git
    git remote add upstream git://github.com/caktus/django-scribbler.git
    git fetch upstream


Running the Tests
------------------------------------

When making changes to the code, either fixing bugs or adding features, you'll want to
run the tests to ensure that you have not broken any of the existing functionality.
With the code checked out and Django installed you can run the tests via::

    python setup.py test

or::

    python runtests.py

Note that the tests require the `mock <http://www.voidspace.org.uk/python/mock/>`_ library.
To test against multiple versions of Django you can use install and use ``tox>=1.4``. The
``tox`` command will run the tests against Django 1.3, 1.4 and the current Git master using
Python 2.6.::

    # Build all environments
    tox
    # Build a single environment
    tox -e py26-1.3.X

Building all environments will also build the documentation. More on that in the next
section.


Building the Documentation
------------------------------------

This project aims to have a minimal core with hooks for customization. That makes documentation
an important part of the project. Useful examples and notes on common use cases are a great
way to contribute and improve the documentation.

The docs are written in `ReST <http://docutils.sourceforge.net/rst.html>`_
and built using `Sphinx <http://sphinx.pocoo.org/>`_. As noted above you can use
tox to build the documentation or you can build them on their own via::

    tox -e docs

or::

    make html

from inside the ``docs/`` directory. 


Building the CSS
------------------------------------

The CSS used by django-scribbler is built using `LESS <http://lesscss.org/>`_. No changes
should be made to the ``scribbler.css`` directly. Instead changes should be made to the ``scribbler.less``
file. After changes are made to ``scribbler.less`` you can create the new CSS with the
Node based complier::

    # Install less from the NPM package
    npm install less -g
    lessc scribbler/static/scribbler/less/scribbler.less > scribbler/static/scribbler/css/scribbler.css

The example project uses the client-side LESS compiler to make local development easier.


Coding Standards
------------------------------------

Code contributions should follow the `PEP8 <http://www.python.org/dev/peps/pep-0008/>`_
and `Django contributing style <https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/>`_
standards. Please note that these are only guidelines. Overall code consistency
and readability are more important than strict adherence to these guides.

The Javascript is configured for some basic `JSHint <http://www.jshint.com/>`_ checks. Changes
to the Javascript should pass without errors. You can check the Javascript file on the command line
with Node based `CLI tool <https://github.com/jshint/jshint>`_::

    # Install jshint from the NPM package
    npm install jshint -g
    # Check the scribbler JS
    jshint scribbler/static/scribbler/js/scribbler.js


Submitting a Pull Request
------------------------------------

The easiest way to contribute code or documentation changes is through a pull request.
For information on submitting a pull request you can read the Github help page
https://help.github.com/articles/using-pull-requests.

Pull requests are a place for the code to be reviewed before it is merged. This review
will go over the coding style as well as if it solves the problem indended and fits
in the scope of the project. It may be a long discussion or it might just be a simple
thank you.

Not necessarily every request will be merged but you should not take it personally
if you change is not accepted. If you want to increase the chances of your change
being incorporated then here are some tips.

- Address a known issue. Preference is given to a request that fixes a currently open issue.
- Include documentation and tests when appropriate. New features should be tested and documented. Bugfixes should include tests which demostrate the problem.
- Keep it simple. It's difficult to review a large block of code so try to keep the scope of the change small.

You should also feel free to ask for help writing tests or writing documentation
if you aren't sure how to go about it.
