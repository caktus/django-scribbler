STATIC_DIR = ./scribbler/static/scribbler
LIBS_DIR = ${STATIC_DIR}/libs
# Library versions
JQUERY_VERSION = 1.8.3
REQUIRE_VERSION = 2.1.4
CODEMIRROR_VERSION = 5.7
BACKBONE_VERSION = 0.9.10
UNDERSCORE_VERSION = 1.4.4


fetch-static-libs:
	# Fetch JS library dependencies
	# Requires curl
	curl -Lo ${LIBS_DIR}/jquery.js http://code.jquery.com/jquery-${JQUERY_VERSION}.js
	curl -Lo ${LIBS_DIR}/require.js http://requirejs.org/docs/release/${REQUIRE_VERSION}/comments/require.js
	curl -Lo ${LIBS_DIR}/backbone.js https://raw.github.com/jashkenas/backbone/${BACKBONE_VERSION}/backbone.js
	curl -Lo ${LIBS_DIR}/underscore.js https://raw.github.com/jashkenas/underscore/${UNDERSCORE_VERSION}/underscore.js
	curl -Lo codemirror-${CODEMIRROR_VERSION}.zip http://codemirror.net/codemirror-${CODEMIRROR_VERSION}.zip
	unzip codemirror-${CODEMIRROR_VERSION}.zip
	rm -rf ${LIBS_DIR}/codemirror
	mkdir -p ${LIBS_DIR}/codemirror
	mv -f codemirror-${CODEMIRROR_VERSION}/* ${LIBS_DIR}/codemirror
	rm -r codemirror-${CODEMIRROR_VERSION}
	rm codemirror-${CODEMIRROR_VERSION}.zip

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
	# Requires r.js optimizer
	cd ${STATIC_DIR}/js && r.js -o name=scribbler out=scribbler-min.js baseUrl=. mainConfigFile=scribbler.js

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
