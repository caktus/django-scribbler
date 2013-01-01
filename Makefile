STATIC_DIR = ./scribbler/static/scribbler

build-css:
	# Build CSS from LESS
	# Requires LESS
	lessc --yui-compress ${STATIC_DIR}/less/scribbler.less ${STATIC_DIR}/css/scribbler.css

lint-js:
	# Check JS for any problems
	# Requires jshint
	jshint ${STATIC_DIR}/js/scribbler.js
	jshint ${STATIC_DIR}/js/djangohint.js

compile-messages:
	# Create compiled .mo files for source distribution
	cd scribbler && django-admin.py compilemessages

make-messages:
	# Create .po message files
	cd scribbler && django-admin.py makemessages -a && django-admin.py makemessages -d djangojs -a

push-messages: make-messages
	# Create messages and push them to Transifex
	# Requires Transifex client
	tx push -s -t

pull-messages:
	# Pull the latest translations from Transifex
	# Requires Transifex client
	tx pull -a

prep-release: lint-js build-css pull-messages compile-messages
	# Prepare for upcoming release
    # Check JS, create CSS, compile translations, run the test suite
	tox
