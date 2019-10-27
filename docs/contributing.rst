Contributing Guide
====================================

There are a number of ways to contribute to django-scribbler. If you are interested
in making django-scribbler better then this guide will help you find a way to contribute.


Ways to Contribute
------------------------------------

You can contribute to the project by submitting bug reports, feature requests
or documentation updates through the Github `issues <https://github.com/caktus/django-scribbler/issues>`_.


Translate django-scribbler
--------------------------------------

We are working towards translating django-scribbler into different languages. There
are only a few strings to translate so it is a great way to be involved with the project.
The translations are managed through `Transifex <https://www.transifex.com/projects/p/django-scribbler/>`_.
Please do not submit translate requests/updates to the Github repo.


Getting the Source
------------------------------------

You can clone the repository from Github::

    git clone https://github.com/caktus/django-scribbler.git

However this checkout will be read only. If you want to contribute code you should
create a fork and clone your fork. You can then add the main repository as a remote::

    git clone git@github.com:<your-username>/django-scribbler.git
    cd django-scribbler
    git remote add upstream git://github.com/caktus/django-scribbler.git
    git fetch upstream

django-scribbler requires a few static libraries which are not included in the repository. Before beginning
development you should make sure you have these libraries with::

    make fetch-static-libs


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
``tox`` command will run the tests against supported versions of Django and Python.::

    # Build all environments
    tox
    # Build a single environment
    tox -e py37-2.2.X

Building all environments will also build the documentation. More on that in the next
section.

The JS plugins are tested using the `QUnit <http://qunitjs.com/>` testing framework. You can
run the tests by opening ``scribbler\tests\qunit\index.html`` in your browser. You can also
run the tests using the `PhantomJS <http://phantomjs.org/>` headless runner. First install
PhantomJS from NPM (requires at least 1.6)::

    # Install phantomjs from the NPM package
    npm install phantomjs -g
    # Run QUnit tests
    phantomjs scribbler/tests/qunit/runner.js scribbler/tests/qunit/index.html

We've added a make command which you can use as well::

    make test-js


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
file. After changes are made to ``scribbler.less`` you can create the new compressed CSS with the
Node based complier. In addition, this inlines the required ``codemirror.css``::

    make build-css

The example project uses the client-side LESS compiler to make local development easier.


Building the JS
------------------------------------

While it is not often needed for local development, the final released JS is bundled and minified
using Browserify and UglifyJS2. To build ``bundle-min.js`` you should
have the optimizer installed and run::

    make build-js


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
    jshint scribbler/static/scribbler/js/

This can also be done with the ``make`` command::

    make lint-js


Submitting a Pull Request
------------------------------------

The easiest way to contribute code or documentation changes is through a pull request.
For information on submitting a pull request you can read the Github help page
https://help.github.com/articles/using-pull-requests.

Pull requests are a place for the code to be reviewed before it is merged. This review
will go over the coding style as well as if it solves the problem intended and fits
in the scope of the project. It may be a long discussion or it might just be a simple
thank you.

Not necessarily every request will be merged but you should not take it personally
if you change is not accepted. If you want to increase the chances of your change
being incorporated then here are some tips.

- Address a known issue. Preference is given to a request that fixes a currently open issue.
- Include documentation and tests when appropriate. New features should be tested and documented. Bugfixes should include tests which demonstrate the problem.
- Keep it simple. It's difficult to review a large block of code so try to keep the scope of the change small.

You should also feel free to ask for help writing tests or writing documentation
if you aren't sure how to go about it.


Installing an Unstable Release
------------------------------------

Since the built CSS, JS and other static dependencies are not included in the repository, it is not
possible to install django-scribbler directly from Github. If you want to install and unstable version
of django-scribbler you have a few options.

.. warning::

    While we try to keep the ``master`` branch stable, there may be bugs or unfinished work there. It
    is recommended that you use a stable release of django-scribbler when possible.


Install Local Build
_____________________________________

The step overview for installing from a local build is:

* Check out the repository
* Install static libraries
* Build CSS and JS
* Install from local repository

From the command line this would be::

    git clone git://github.com/caktus/django-scribbler.git
    cd django-scribbler
    make fetch-static-libs build-css build-js


Create an Unstable Package
_____________________________________

Installing from a local build is probably a reasonable solution for a single person wanting
to test out the current master or a feature branch in a large project. However, it isn't a good
solution if you want to deploy this to a larger testing environment or multiple computers. The
basic steps are more or less the same:

* Check out the repository
* Install static libraries
* Build CSS and JS
* Create a source distribution
* Distribute .tar file
* Install for packaged .tar

From the command line this would be::

    git clone git://github.com/caktus/django-scribbler.git
    cd django-scribbler
    make fetch-static-libs build-css build-js
    python setup.py sdist

This will create a ``django-scribbler-X.X.X.tar.gz`` inside a ``dist/`` directory where
``X.X.X`` is the current ``scribbler.__version__``. This tar file would then be distributed
using your favorite file hosting service (S3, Dropbox, etc). You can then install by using ``pip``::

    pip install http://path-to-hostedfile/django-scribbler-X.X.X.tar.gz
