/* imposter (OO.org Impress viewer)
** Copyright (C) 2003 Gurer Ozen <madcat@e-kolay.net>
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"

static GtkWidget *win;

void
about_show (void)
{
	GtkWidget *lab, *b;
	char *text;

	if (win) {
		gtk_window_present (GTK_WINDOW (win));
		return;
	}

	win = gtk_dialog_new ();
	gtk_window_set_position (GTK_WINDOW (win), GTK_WIN_POS_CENTER);
	gtk_window_set_resizable (GTK_WINDOW (win), FALSE);
	gtk_window_set_title (GTK_WINDOW (win), _("About this fine product..."));
	g_signal_connect (G_OBJECT (win), "delete_event", G_CALLBACK (gtk_widget_hide_on_delete), NULL);

	lab = gtk_label_new (NULL);
	gtk_widget_show (lab);
	gtk_misc_set_padding (GTK_MISC (lab), 6, 6);
	gtk_label_set_justify (GTK_LABEL (lab), GTK_JUSTIFY_CENTER);
	text = g_strdup_printf (_("<span size='x-large'><b>imposter %s</b></span>\n\n"
		"Copyright (c) 2003 G\xC3\xBCrer \xC3\x96zen\n"
		"<span size='small'>This program is free software; you can redistribute and/or\n"
		"modify it under the terms of the GNU General Public License.</span>\n\n"
		"http://imposter.sourceforge.net"),VERSION);
	gtk_label_set_markup (GTK_LABEL (lab), text);
	g_free (text);
	gtk_box_pack_start (GTK_BOX (GTK_DIALOG (win)->vbox), lab, TRUE, TRUE, 0);

	b = gtk_button_new_from_stock (GTK_STOCK_OK);
	gtk_widget_show (b);
	gtk_box_pack_end (GTK_BOX (GTK_DIALOG (win)->action_area), b, FALSE, TRUE, 0);
	GTK_WIDGET_SET_FLAGS (b, GTK_CAN_DEFAULT);
	gtk_widget_grab_focus (b);
	g_signal_connect_swapped (G_OBJECT (b), "clicked", G_CALLBACK (gtk_widget_hide), G_OBJECT (win));

	gtk_widget_show (win);
}
