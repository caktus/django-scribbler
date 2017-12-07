STATIC_DIR = ./scribbler/static/scribbler
PROJECT_FILES = ${STATIC_DIR}/js/scribbler-main.js ${STATIC_DIR}/js/scribbler-editor.js ${STATIC_DIR}/js/scribbler-menu.js ${STATIC_DIR}/js/djangohint.js
TESTS_DIR = ./scribbler/tests/qunit
TEST_FILES = ${TESTS_DIR}/menu-test.js ${TESTS_DIR}/editor-test.js

fetch-static-libs: FORCE
	# Fetch JS library dependencies
	# Requires npm
	npm install
	npm update
FORCE:

${STATIC_DIR}/css/scribbler.css: ${STATIC_DIR}/less/scribbler.less fetch-static-libs
	# Build CSS from LESS
	# Requires LESS
	mkdir -p ${STATIC_DIR}/css
	echo | node_modules/.bin/lessc -x node_modules/codemirror/lib/codemirror.css > $@
	echo $^ $@
	echo | node_modules/.bin/lessc ${STATIC_DIR}/less/scribbler.less >> $@

build-css: ${STATIC_DIR}/css/scribbler.css

lint-js: fetch-static-libs
	# Check JS for any problems
	node_modules/.bin/jshint ${STATIC_DIR}/js/djangohint.js
	node_modules/.bin/jshint ${STATIC_DIR}/js/scribbler-main.js
	node_modules/.bin/jshint ${STATIC_DIR}/js/scribbler-editor.js
	node_modules/.bin/jshint ${STATIC_DIR}/js/scribbler-menu.js
	node_modules/.bin/jshint ${STATIC_DIR}/js/plugins/

${STATIC_DIR}/js/scribbler.js: ${PROJECT_FILES}
	node_modules/.bin/browserify $< -o $@

${STATIC_DIR}/js/scribbler-min.js: ${STATIC_DIR}/js/scribbler.js
	node_modules/.bin/uglifyjs $^ -o $@

build-js: ${STATIC_DIR}/js/scribbler-min.js

${TESTS_DIR}/bundle.js: ${TESTS_DIR}/main.js ${PROJECT_FILES} ${TEST_FILES}
	node_modules/.bin/browserify -t browserify-compile-templates --extension=.html $< -o $@

test-js: ${TESTS_DIR}/bundle.js
	# Run the QUnit tests
	# Requires PhantomJS
	node_modules/.bin/phantomjs ${TESTS_DIR}/runner.js ${TESTS_DIR}/index.html

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

dist: clean fetch-static-libs lint-js build-js build-css
	python setup.py sdist
	python setup.py bdist_wheel --universal

clean:
	rm -f ${STATIC_DIR}/js/scribbler.js
	rm -f ${STATIC_DIR}/js/scribbler-min.js
	rm -rf ${STATIC_DIR}/css
	rm -f ${TESTS_DIR}/bundle.js
	rm -rf example/example/static/
	rm -rf dist
	rm -rf .tox
	rm -rf node_modules

.PHONY: build-css build-js lint-js test-js compile-messages make-messages push-messages pull-messages prep-release dist clean
