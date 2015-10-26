STATIC_DIR = ./scribbler/static/scribbler
# Library versions
JQUERY_VERSION = 1.8.3
REQUIRE_VERSION = 2.1.4
CODEMIRROR_VERSION = 5.7
BACKBONE_VERSION = 0.9.10
UNDERSCORE_VERSION = 1.4.4


fetch-static-libs:
	# Fetch JS library dependencies
	# Requires npm
	mkdir -p ${STATIC_DIR}/node_modules
	cd ${STATIC_DIR} && npm install jquery
	cd ${STATIC_DIR} && npm install underscore
	cd ${STATIC_DIR} && npm install backbone
	cd ${STATIC_DIR} && npm install codemirror

build-css:
	# Build CSS from LESS
	# Requires LESS and r.js optimizer
	mkdir -p ${STATIC_DIR}/css
	lessc -x ${STATIC_DIR}/less/scribbler.less ${STATIC_DIR}/css/scribbler.css
	cd ${STATIC_DIR}/css && r.js -o cssIn=scribbler.css out=scribbler.css

lint-js:
	# Check JS for any problems
	# Requires jshint
	jshint ${STATIC_DIR}/js/djangohint.js
	jshint ${STATIC_DIR}/js/scribbler.js
	jshint ${STATIC_DIR}/js/scribbler-editor.js
	jshint ${STATIC_DIR}/js/scribbler-menu.js
	jshint ${STATIC_DIR}/js/plugins/

build-js:
	# Build optimized JS
	# Requires browserify
	# Requires uglifyjs
	cd ${STATIC_DIR}/js && browserify scribbler.js -o bundle.js
	cd ${STATIC_DIR}/js && browserify scribbler.js | uglifyjs -o bundle-min.js

test-js:
	# Run the QUnit tests
	# Requires PhantomJS
	phantomjs scribbler/tests/qunit/runner.js scribbler/tests/qunit/index.html

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

prep-release: lint-js build-css build-js pull-messages compile-messages
	# Prepare for upcoming release
    # Check JS, create CSS, compile translations, run the test suite
	tox
