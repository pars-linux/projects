/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#ifndef COMMON_H
#define COMMON_H 1

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <sys/types.h>
#include <stdio.h>

#ifdef STDC_HEADERS
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#elif HAVE_STRINGS_H
#include <strings.h>
#endif

#ifdef HAVE_UNISTD_H
#include <unistd.h>
#endif

#ifdef HAVE_ERRNO_H
#include <errno.h>
#endif
#ifndef errno
extern int errno;
#endif

#include <gtk/gtk.h>
#include <iksemel.h>
#include "i18n.h"
#include "imposter.h"

void main_quit(void);

void ui_setup (void);
void ui_open (const char *filename);
void ui_toggle_fs (void);
void page_first (void);
void page_next (void);
void page_prev (void);
void page_last (void);

void slave_start (void);

void about_show (void);

void info_setup (void);
void info_show (void);

void debug_show(void);
void debug_update(ImpDoc *doc);
void debug_clean(void);

typedef void (sf_func)(char *filename, gpointer data);
GtkWidget *sf_new (gboolean for_save, GtkWidget *main_window, char *title, sf_func *func);
void sf_ask (GtkWidget *sfw, gpointer data);

void draw_bezier (GdkDrawable *d, GdkGC *gc, int x0, int y0, int x1, int y1, int x2, int y2, int x3, int y3);


#endif	/* COMMON_H */
