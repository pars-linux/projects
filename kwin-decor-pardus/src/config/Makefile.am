INCLUDES = $(all_includes)

kde_module_LTLIBRARIES = kwin_PARDUS_config.la

kwin_PARDUS_config_la_SOURCES = config.cpp configdialog.ui
kwin_PARDUS_config_la_LDFLAGS = $(all_libraries) $(KDE_PLUGIN) -module
kwin_PARDUS_config_la_LIBADD = $(LIB_KDEUI) $(LIB_KIO)

METASOURCES = AUTO
noinst_HEADERS = config.h
DISTCLEANFILES = $(METASOURCES)

lnkdir = $(kde_datadir)/kwin

