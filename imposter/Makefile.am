##
## Process this file with automake to produce Makefile.in
##

SUBDIRS = include src po

EXTRA_DIST = config.rpath ABOUT-NLS depcomp

snapshot:
	$(MAKE) dist distdir=$(PACKAGE)-`date +"%y%m%d"`
	mv $(PACKAGE)-`date +"%y%m%d"`.tar.gz ../
