# Based on https://spin.atomicobject.com/2015/11/30/command-line-tools-docker/
PREFIX ?= /usr/local
REPO = "utulsa/wpe-tool"
VERSION = "0.1"

all: build

build:
	@docker build -t $(REPO):$(VERSION) . \
	&& docker tag $(REPO):$(VERSION) $(REPO):latest

install: build
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	install -m 0755 wpe-tool $(DESTDIR)$(PREFIX)/bin/wpe-tool

uninstall:
	@$(RM) $(DESTDIR)$(PREFIX)/bin/wpe-deploy
	@docker rmi $(REPO):$(VERSION)
	@docker rmi $(REPO):latest
