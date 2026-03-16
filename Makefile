# cc-docs — Claude Code Documentation PDF Generator
#
# Usage:
#   make              Build both languages (en + zh-TW)
#   make LANG=en      Build English only
#   make LANG=zh-TW   Build Traditional Chinese only
#   make clean        Remove all build artifacts
#
# Individual pipeline steps (same LANG parameter):
#   make download     Fetch docs from code.claude.com
#   make merge        Combine into single markdown
#   make pdf          Generate PDF from merged markdown

# Only override when LANG is passed on the command line (not from env)
ifeq ($(origin LANG),command line)
LANGS := $(LANG)
else
LANGS := en zh-TW
endif

BASEDIR := .

.PHONY: build download merge pdf clean

build: download merge pdf

download:
	@for lang in $(LANGS); do \
		echo "==> Downloading $$lang docs..."; \
		python3 scripts/download_md.py --lang "$$lang" --basedir $(BASEDIR); \
	done

merge:
	@for lang in $(LANGS); do \
		echo "==> Merging $$lang docs..."; \
		python3 scripts/merge_docs.py --lang "$$lang" --basedir $(BASEDIR); \
	done

pdf:
	@for lang in $(LANGS); do \
		echo "==> Generating $$lang PDF..."; \
		python3 scripts/generate_pdf.py --lang "$$lang" --basedir $(BASEDIR); \
	done

clean:
	rm -rf build/
	rm -rf output/
	rm -rf dist/
	rm -rf scripts/__pycache__/
