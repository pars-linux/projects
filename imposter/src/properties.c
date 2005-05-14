/* imposter (OO.org Impress viewer)
** Copyright (C) 2003 Gurer Ozen <madcat@e-kolay.net>
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"

static GtkWidget *win, *w_author, *w_generator, *w_date;

static void
info_clean (void)
{
	gtk_label_set_text (GTK_LABEL (w_author), "");
	gtk_label_set_text (GTK_LABEL (w_generator), "");
	gtk_label_set_text (GTK_LABEL (w_date), "");
	return;
}

static void
info_update (void)
{
	iks *x;
	char *tmp;

	x = iks_find (oo_doc_get_xml (doc, "meta.xml"), "office:meta");

	tmp = iks_find_cdata (x, "meta:initial-creator");
	if (NULL == tmp) tmp = "";
	gtk_label_set_text (GTK_LABEL (w_author), tmp);

	tmp = iks_find_cdata (x, "meta:generator");
	if (NULL == tmp) tmp = "";
	gtk_label_set_text (GTK_LABEL (w_generator), tmp);

	tmp = iks_find_cdata (x, "dc:date");
	if (NULL == tmp) tmp = "";
	gtk_label_set_text (GTK_LABEL (w_date), tmp);
}

void
info_setup (void)
{
	GtkWidget *vb, *table, *lab, *sep, *bb, *but;

	win = gtk_window_new (GTK_WINDOW_TOPLEVEL);
	gtk_window_set_title (GTK_WINDOW (win), _("Properties"));
	gtk_window_set_default_size (GTK_WINDOW (win), 265, 145);
	g_signal_connect (G_OBJECT (win), "delete_event", G_CALLBACK (gtk_widget_hide_on_delete), NULL);

	vb = gtk_vbox_new (FALSE, 0);
	gtk_widget_show (vb);
	gtk_container_set_border_width (GTK_CONTAINER (vb), 6);
	gtk_container_add (GTK_CONTAINER (win), vb);

	table = gtk_table_new (3, 2, FALSE);
	gtk_widget_show (table);
	gtk_table_set_col_spacings (GTK_TABLE (table), 6);
	gtk_table_set_row_spacings (GTK_TABLE (table), 6);
	gtk_container_set_border_width (GTK_CONTAINER (table), 6);
	gtk_box_pack_start (GTK_BOX (vb), table, TRUE, TRUE, 0);

	lab = gtk_label_new (NULL);
	gtk_label_set_markup (GTK_LABEL (lab), _("<b>Author:</b>"));
	gtk_misc_set_alignment (GTK_MISC (lab), 1, 0.5);
	gtk_widget_show (lab);
	gtk_table_attach (GTK_TABLE (table), lab, 0, 1, 0, 1, GTK_SHRINK | GTK_FILL, GTK_SHRINK | GTK_FILL, 0, 0);

	w_author = gtk_label_new (NULL);
	gtk_label_set_selectable (GTK_LABEL (w_author), TRUE);
	gtk_misc_set_alignment (GTK_MISC (w_author), 0, 0.5);
	gtk_widget_show (w_author);
	gtk_table_attach (GTK_TABLE (table), w_author, 1, 2, 0, 1, GTK_EXPAND | GTK_FILL, GTK_FILL, 0, 0);

	lab = gtk_label_new (NULL);
	gtk_label_set_markup (GTK_LABEL (lab), _("<b>Software:</b>"));
	gtk_misc_set_alignment (GTK_MISC (lab), 1, 0.5);
	gtk_widget_show (lab);
	gtk_table_attach (GTK_TABLE (table), lab, 0, 1, 1, 2, GTK_SHRINK | GTK_FILL, GTK_SHRINK | GTK_FILL, 0, 0);

	w_generator = gtk_label_new (NULL);
	gtk_label_set_selectable (GTK_LABEL (w_generator), TRUE);
	gtk_misc_set_alignment (GTK_MISC (w_generator), 0, 0.5);
	gtk_widget_show (w_generator);
	gtk_table_attach (GTK_TABLE (table), w_generator, 1, 2, 1, 2, GTK_EXPAND | GTK_FILL, GTK_FILL, 0, 0);

	lab = gtk_label_new (NULL);
	gtk_label_set_markup (GTK_LABEL (lab), _("<b>Date:</b>"));
	gtk_misc_set_alignment (GTK_MISC (lab), 1, 0.5);
	gtk_widget_show (lab);
	gtk_table_attach (GTK_TABLE (table), lab, 0, 1, 2, 3, GTK_SHRINK | GTK_FILL, GTK_SHRINK | GTK_FILL, 0, 0);

	w_date = gtk_label_new (NULL);
	gtk_label_set_selectable (GTK_LABEL (w_date), TRUE);
	gtk_misc_set_alignment (GTK_MISC (w_date), 0, 0.5);
	gtk_widget_show (w_date);
	gtk_table_attach (GTK_TABLE (table), w_date, 1, 2, 2, 3, GTK_EXPAND | GTK_FILL, GTK_FILL, 0, 0);

	sep = gtk_hseparator_new ();
	gtk_widget_show (sep);
	gtk_box_pack_start (GTK_BOX (vb), sep, FALSE, FALSE, 6);

	bb = gtk_hbutton_box_new ();
	gtk_widget_show (bb);
	gtk_button_box_set_layout (GTK_BUTTON_BOX (bb), GTK_BUTTONBOX_END);
	gtk_box_set_spacing (GTK_BOX (bb), 6);
	gtk_container_set_border_width (GTK_CONTAINER (bb), 6);
	gtk_box_pack_start (GTK_BOX (vb), bb, FALSE, FALSE, 0);

	but = gtk_button_new_from_stock (GTK_STOCK_CLOSE);
	gtk_widget_show (but);
	gtk_container_add (GTK_CONTAINER (bb), but);
	g_signal_connect_swapped (G_OBJECT (but), "clicked", G_CALLBACK (gtk_widget_hide), (gpointer)win);

	g_signal_connect (G_OBJECT (doc), "doc-open", G_CALLBACK (info_update), NULL);
	g_signal_connect (G_OBJECT (doc), "doc-close", G_CALLBACK (info_clean), NULL);
}

void
info_show (void)
{
	gtk_window_present (GTK_WINDOW (win));
}
