SHELL :=/bin/bash

POSTS_DIR=hugo/content/posts
IPYNB_FILES=$(wildcard notebooks/*.ipynb)
MARKDOWN_FILES_TO_BUILD=$(patsubst notebooks/%.ipynb, $(POSTS_DIR)/%.md, $(IPYNB_FILES))
RUN=poetry run

# Rule to build markdown files from jupyter notebooks
$(POSTS_DIR)/%.md: notebooks/%.ipynb
	@echo Building '$<' in $@
	$(RUN) nb2hugo --site-dir hugo --section posts $<

src/requirements.txt: poetry.lock
	poetry export -f requirements.txt --without-hashes > src/requirements.txt

build: ;

.PHONY: install-deps
install-deps:
	poetry lock
	poetry install --remove-untracked

.PHONY: test
test: build
	$(RUN) pytest test

.PHONY: build-sam
build-sam:
	$(RUN) sam build

.PHONY: deploy
deploy: src/requirements.txt build-sam
	$(RUN) sam deploy

.DEFAULT_GOAL := default
default: build install-deps test build-sam
