NAME = virt-wrapper
VERSION = 0.1.1

DIST_FILES = \
	 AUTHORS \
	 ChangeLog \
	 COPYING \
	 Makefile \
	 README \
	 po/*.po* \
	 *.py

MO_FILES := $(patsubst %.po,%.mo,$(wildcard po/*.po))

all:	$(MO_FILES)

clean:
	rm -f po/*.mo

dist:
	mkdir $(NAME)-$(VERSION)
	for f in $(DIST_FILES); do \
		install -D -m 644 $$f $(NAME)-$(VERSION)/$$f; \
	done
	tar czvf $(NAME)-$(VERSION).tar.gz $(NAME)-$(VERSION) --exclude .svn
	rm -rf $(NAME)-$(VERSION)

install:	all
	install -D -m 755 virt-wrapper.py $(DESTDIR)/usr/libexec/virt-wrapper
	for m in po/*.mo; do \
		install -D -m 644 $$m $(DESTDIR)/usr/share/locale/`basename $$m .mo`/LC_MESSAGES/virt-wrapper.mo; \
	done

update_messages:
	xgettext -o po/virt-wrapper.pot *.py
	for p in po/*.po; do \
		msgmerge --update $$p po/virt-wrapper.pot; \
	done

po/%.mo:	po/%.po
	msgfmt --statistics -o $@ $<
