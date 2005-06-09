/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"

static void
cb_filesel (GtkDialog *dialog, gint arg1, sf_func *func)
{
	char *name;
	gpointer data;

	if (arg1 == GTK_RESPONSE_ACCEPT) {
		name = gtk_file_chooser_get_filename (GTK_FILE_CHOOSER (dialog));
		data = g_object_get_data (G_OBJECT (dialog), "data");
		func (name, data);
		g_free (name);
	}
	gtk_widget_hide (GTK_WIDGET (dialog));
}

GtkWidget *
sf_new (gboolean for_save, GtkWidget *main_window, char *title, sf_func *func)
{
	GtkWidget *dialog;
	GtkFileChooserAction mode;

	if (for_save)
		mode = GTK_FILE_CHOOSER_ACTION_SAVE;
	else
		mode = GTK_FILE_CHOOSER_ACTION_OPEN;

	dialog = gtk_file_chooser_dialog_new (
		title,
		GTK_WINDOW (main_window),
		mode,
		GTK_STOCK_CANCEL, GTK_RESPONSE_CANCEL,
		for_save ? GTK_STOCK_SAVE : GTK_STOCK_OPEN, GTK_RESPONSE_ACCEPT,
		NULL
	);
	g_signal_connect (dialog, "response", G_CALLBACK (cb_filesel), func);
	return dialog;
}

void
sf_ask (GtkWidget *sfw, gpointer data)
{
	g_object_set_data (G_OBJECT (sfw), "data", data);
	gtk_widget_show (sfw);
}

void
draw_bezier (GdkDrawable *d, GdkGC *gc, int x0, int y0, int x1, int y1, int x2, int y2, int x3, int y3)
{
	int x, y, nx, ny;
	int ax, bx, cx, ay, by, cy;
	double t, t2, t3;

	x = x0;
	y = y0;

	cx = 3 * (x1 - x0);
	bx = 3 * (x2 - x1) - cx;
	ax = x3 - x0 - cx - bx;
	cy = 3 * (y1 - y0);
	by = 3 * (y2 - y1) - cy;
	ay = y3 - y0 - cy - by;

	for (t = 0; t < 1; t += 0.01) {
		t2 = t * t;
		t3 = t2 * t;
		nx = ax * t3 + bx * t2 + cx * t + x0;
		ny = ay * t3 + by * t2 + cy * t + y0;
		gdk_draw_line (d, gc, x, y, nx, ny);
		x = nx;
		y = ny;
	}
}
