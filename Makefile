STATIC_DIR = ./scribbler/static/scribbler

fetch-static-libs:
	# Fetch JS library dependencies
	# Requires npm
	npm install

${STATIC_DIR}/css/scribbler.css: ${STATIC_DIR}/less/scribbler.less
	# Build CSS from LESS
	# Requires LESS and r.js optimizer
	mkdir -p ${STATIC_DIR}/css
	lessc -x $^ $@
	r.js -o cssIn=$@ out=$@

build-css: ${STATIC_DIR}/css/scribbler.css

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
	cd ./scribbler/tests/qunit && browserify -t browserify-compile-templates --extension=.html main.js -o bundle.js

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

.PHONY: build-css build-js lint-js test-js compile-messages make-messages push-messages pull-messages prep-release
