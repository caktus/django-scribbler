STATIC_DIR = ./scribbler/static/scribbler

build-css:
	# Build CSS from LESS
	# Requires LESS
	lessc --yui-compress ${STATIC_DIR}/less/scribbler.less ${STATIC_DIR}/css/scribbler.css

lint-js:
	# Check JS for any problems
	jshint ${STATIC_DIR}/js/scribbler.js
	jshint ${STATIC_DIR}/js/djangohint.js

compile-messages:
	# Create compiled .mo files for source distribution
	cd scribbler && django-admin.py compilemessages
