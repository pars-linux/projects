INCLUDES = -I$(top_srcdir) $(all_includes)

SUBDIRS = config

kde_module_LTLIBRARIES = kwin3_PARDUS.la

kwin3_PARDUS_la_SOURCES = PARDUS.cpp PARDUSclient.cpp PARDUSbutton.cpp misc.cpp shadow.cpp

kwin3_PARDUS_la_LIBADD = $(LIB_KDEUI) -lkdecorations
kwin3_PARDUS_la_LDFLAGS = $(all_libraries) $(KDE_PLUGIN) -module
METASOURCES = AUTO

linkdir = $(kde_datadir)/kwin/
link_DATA = PARDUS.desktop

kwin_pics_data_DATA = titlebar_decor.png konqui-deco.png
kwin_pics_datadir = $(kde_datadir)/kwin/pics

EXTRA_DIST = $(kwin_pics_data_DATA) $(link_DATA) $(kdisplay_colorscheme_DATA)

COMMAND=$(XGETTEXT) --foreign-user -C -ci18n -ki18n -ktr2i18n -kI18N_NOOP -kI18N_NOOP2 -kaliasLocale
messages:
	$(COMMAND) *.cpp config/*.cpp -o ../po/kwin_PARDUS.pot
