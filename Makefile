LOCALES_DIR := src/tbr/locales
POT_FILE := $(LOCALES_DIR)/messages.pot
DOMAIN := messages
LANGS := fr_FR en_US

.PHONY: all pot update compile i18n

all: i18n

pot:
	xgettext --language=Python \
	         --keyword=_ \
	         --output=$(POT_FILE) \
	         src/tbr/*.py

update: pot
	for lang in $(LANGS); do \
	  msgmerge --update --backup=none $(LOCALES_DIR)/$$lang/LC_MESSAGES/$(DOMAIN).po $(POT_FILE); \
	done

compile:
	for lang in $(LANGS); do \
	  msgfmt --output-file=$(LOCALES_DIR)/$$lang/LC_MESSAGES/$(DOMAIN).mo \
	         $(LOCALES_DIR)/$$lang/LC_MESSAGES/$(DOMAIN).po; \
	done

i18n: pot update compile
	@echo "Internationalization done"
