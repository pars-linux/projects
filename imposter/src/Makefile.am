##
## Process this file with automake to produce Makefile.in
##

datadir = @datadir@
localedir = $(datadir)/locale
DEFS = -DLOCALEDIR=\"$(localedir)\" @DEFS@
INCLUDES = -I$(top_srcdir)/include -I$(top_builddir)/include $(GTK_CFLAGS) $(IKSEMEL_CFLAGS) $(INTLDIR)

EXTRA_DIST = iksemel.c

if DO_IKSEMEL
iksemel_c = iksemel.c
endif

bin_PROGRAMS = imposter

imposter_SOURCES = \
	main.c \
	ui.c \
	slave.c \
	about.c \
	gtkutility.c \
	properties.c \
	debug.c \
	document.c \
	render.c \
	r_page.c \
	r_draw.c \
	r_gradient.c \
	r_geometry.c \
	r_text.c \
	r_style.c \
	r_image.c \
	r_path.c \
	zip.c \
	$(iksemel_c)

imposter_LDADD = $(GTK_LIBS) $(IKSEMEL_LIBS) $(INTLLIBS)
