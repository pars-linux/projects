/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"

enum {
	COL_NODE,
	N_COLS
};

static GtkWidget *win;
static GtkWidget *w_path, *w_list, *w_label, *w_data;
static GtkListStore *list_store;
static iks *cur_node;
static ImpDoc *cur_doc;

static void
update_path (iks *def)
{
	iks *x;
	GtkTreeIter iter;
	char *text, *name, *tmp;

	/* update path string */
	x = cur_node;
	text = NULL;
	while (x) {
		if (iks_type (x) == IKS_TAG) {
			name = iks_name (x);
		} else {
			name = "(cdata)";
		}
		if (text) {
			tmp = g_strconcat ("/", name, text, NULL);
			g_free (text);
			text = tmp;
		} else {
			text = g_strconcat ("/", name, NULL);
		}
		x = iks_parent (x);
	}
	gtk_entry_set_text (GTK_ENTRY (w_path), text);
	gtk_editable_set_position (GTK_EDITABLE (w_path), -1);
	g_free (text);

	/* update child list */
	gtk_list_store_clear (list_store);
	gtk_list_store_append (list_store, &iter);
	gtk_list_store_set (list_store, &iter, COL_NODE, NULL, -1);
	for (x = iks_child (cur_node); x; x = iks_next (x)) {
		gtk_list_store_append (list_store, &iter);
		gtk_list_store_set (list_store, &iter, COL_NODE, (gpointer) x, -1);
		if (x == def) {
			char *str;
			GtkTreePath *path;
			str = gtk_tree_model_get_string_from_iter (GTK_TREE_MODEL (list_store), &iter);
			path = gtk_tree_path_new_from_string (str);
			gtk_tree_view_set_cursor (GTK_TREE_VIEW (w_list), path, NULL, FALSE);
			gtk_tree_path_free (path);
			g_free (str);
		}
	}
}

void
debug_update(ImpDoc *doc)
{
	cur_doc = doc;
	cur_node = imp_get_xml(cur_doc, "content.xml");
	update_path(iks_child(cur_node));
}

void
debug_clean(void)
{
	gtk_entry_set_text(GTK_ENTRY(w_path), "");
	gtk_list_store_clear(list_store);
	gtk_label_set_text(GTK_LABEL(w_label), "");
	gtk_text_buffer_set_text(gtk_text_view_get_buffer(GTK_TEXT_VIEW(w_data)), "", 0);
	cur_node = NULL;
	cur_doc = NULL;
}

static void
cb_parent (void)
{
	if (cur_node) {
		iks *x, *old;
		x = iks_parent (cur_node);
		if (x) {
			old = cur_node;
			cur_node = x;
			update_path (old);
		}
	}
}

static void
cb_content (void)
{
	if (cur_doc) {
		cur_node = imp_get_xml(cur_doc, "content.xml");
		update_path(iks_child(cur_node));
	}
}

static void
cb_styles (void)
{
	if (cur_doc) {
		cur_node = imp_get_xml(cur_doc, "styles.xml");
		update_path(iks_child(cur_node));
	}
}

static void
cb_meta (void)
{
	if (cur_doc) {
		cur_node = imp_get_xml(cur_doc, "meta.xml");
		update_path(iks_child(cur_node));
	}
}

static void
cb_settings (void)
{
	if (cur_doc) {
		cur_node = imp_get_xml(cur_doc, "settings.xml");
		update_path(iks_child(cur_node));
	}
}

static void
cb_row_activated (GtkTreeView *view, GtkTreePath *path, GtkTreeViewColumn *col, gpointer data)
{
	iks *node;
	GtkTreeIter iter;

	if (gtk_tree_model_get_iter (GTK_TREE_MODEL (list_store), &iter, path)) {
		gtk_tree_model_get (GTK_TREE_MODEL (list_store), &iter, COL_NODE, &node, -1);
		if (node) {
			if (iks_type (node) == IKS_TAG) {
				cur_node = node;
				update_path (iks_child (cur_node));
			}
		} else {
			cb_parent ();
		}
	}
}

static void
cb_cursor (void)
{
	iks *node;
	GtkTreePath *path;
	GtkTreeIter iter;

	gtk_tree_view_get_cursor (GTK_TREE_VIEW (w_list), &path, NULL);
	if (gtk_tree_model_get_iter (GTK_TREE_MODEL (list_store), &iter, path)) {
		gtk_tree_model_get (GTK_TREE_MODEL (list_store), &iter, COL_NODE, &node, -1);
		if (0 == node) node = cur_node;
		if (iks_type (node) == IKS_TAG) {
			char *text, *tmp;
			iks *x;
			text = g_strdup_printf (_("<b>Tag name</b>: %s"), iks_name (node));
			gtk_label_set_markup (GTK_LABEL (w_label), text);
			g_free (text);
			text = NULL;
			for (x = iks_attrib (node); x; x = iks_next (x)) {
				if (text) {
					tmp = g_strconcat (text, "\n", iks_name (x), " = ", iks_cdata (x), NULL);
					g_free (text);
					text = tmp;
				} else
					text = g_strconcat (iks_name (x), " = ", iks_cdata (x), NULL);
			}
			if (text) {
				gtk_text_buffer_set_text (gtk_text_view_get_buffer (GTK_TEXT_VIEW (w_data)), text, strlen (text));
				g_free (text);
			} else {
				gtk_text_buffer_set_text (gtk_text_view_get_buffer (GTK_TEXT_VIEW (w_data)), "", 0);
			}
		} else {
			gtk_label_set_markup (GTK_LABEL (w_label), _("<b>Character data node</b>"));
			gtk_text_buffer_set_text (gtk_text_view_get_buffer (GTK_TEXT_VIEW (w_data)),
				iks_cdata (node), iks_cdata_size (node));
		}
	}
}

static void
cb_render_node (GtkTreeViewColumn *col, GtkCellRenderer *rend, GtkTreeModel *model, GtkTreeIter *iter, gpointer udata)
{
	iks *node;
	char *name;

	gtk_tree_model_get (GTK_TREE_MODEL (list_store), iter, COL_NODE, &node, -1);
	if (0 == node) {
		name = "/";
	} else if (iks_type (node) == IKS_TAG) {
		name = iks_name (node);
	} else {
		name = "(cdata)";
	}
	g_object_set (rend, "text", name, NULL);
}

void
debug_show (void)
{
	GtkWidget *vb, *hb, *vb2, *but, *sw;
	GtkCellRenderer *rend;
	GtkTreeViewColumn *col;

	if (win) {
		gtk_window_present (GTK_WINDOW (win));
		return;
	}

	win = gtk_window_new (GTK_WINDOW_TOPLEVEL);
	gtk_window_set_title (GTK_WINDOW (win), _("XML Browser"));
	gtk_window_set_default_size (GTK_WINDOW (win), 400, 380);
	g_signal_connect (G_OBJECT (win), "delete_event", G_CALLBACK (gtk_widget_hide_on_delete), NULL);

	vb = gtk_vbox_new (FALSE, 6);
	gtk_widget_show (vb);
	gtk_container_set_border_width (GTK_CONTAINER (vb), 6);
	gtk_container_add (GTK_CONTAINER (win), vb);

	/* path string and parent button */
	hb = gtk_hbox_new (FALSE, 6);
	gtk_widget_show (hb);
	gtk_box_pack_start (GTK_BOX (vb), hb, FALSE, FALSE, 0);

	w_path = gtk_entry_new ();
	gtk_entry_set_editable (GTK_ENTRY (w_path), FALSE);
	gtk_widget_show (w_path);
	gtk_box_pack_start (GTK_BOX (hb), w_path, TRUE, TRUE, 0);

	but = gtk_button_new_with_mnemonic (_("_Parent"));
	gtk_widget_show (but);
	gtk_box_pack_start (GTK_BOX (hb), but, FALSE, FALSE, 0);
	g_signal_connect (G_OBJECT (but), "clicked", G_CALLBACK (cb_parent), NULL);

	/* child list and node information area */
	hb = gtk_hbox_new (FALSE, 6);
	gtk_widget_show (hb);
	gtk_box_pack_start (GTK_BOX (vb), hb, TRUE, TRUE, 0);

	sw = gtk_scrolled_window_new (NULL, NULL);
	gtk_widget_show (sw);
	gtk_scrolled_window_set_policy (GTK_SCROLLED_WINDOW (sw), GTK_POLICY_NEVER, GTK_POLICY_AUTOMATIC);
	gtk_scrolled_window_set_shadow_type (GTK_SCROLLED_WINDOW (sw), GTK_SHADOW_ETCHED_IN);
	gtk_box_pack_start (GTK_BOX(hb), sw, FALSE, FALSE, 0);

	list_store = gtk_list_store_new (N_COLS, G_TYPE_POINTER);
	w_list = gtk_tree_view_new_with_model (GTK_TREE_MODEL (list_store));
	gtk_tree_view_set_headers_visible (GTK_TREE_VIEW (w_list), FALSE);
	rend = gtk_cell_renderer_text_new ();
	col = gtk_tree_view_column_new_with_attributes (NULL, rend, NULL);
	gtk_tree_view_append_column (GTK_TREE_VIEW (w_list), col);
	gtk_tree_view_column_set_cell_data_func (col, rend, cb_render_node, NULL, NULL);
	gtk_widget_show (w_list);
	gtk_container_add (GTK_CONTAINER (sw), w_list);
	g_signal_connect (G_OBJECT(w_list), "row_activated", G_CALLBACK (cb_row_activated), NULL);
	g_signal_connect (G_OBJECT(w_list), "cursor_changed", G_CALLBACK (cb_cursor), NULL);

	vb2 = gtk_vbox_new (FALSE, 6);
	gtk_widget_show (vb2);
	gtk_box_pack_start (GTK_BOX (hb), vb2, TRUE, TRUE, 0);

	w_label = gtk_label_new (NULL);
	gtk_widget_show (w_label);
	gtk_misc_set_alignment (GTK_MISC (w_label), 0, 0.5);
	gtk_box_pack_start (GTK_BOX (vb2), w_label, FALSE, FALSE, 0);

	sw = gtk_scrolled_window_new (NULL, NULL);
	gtk_widget_show (sw);
	gtk_scrolled_window_set_policy (GTK_SCROLLED_WINDOW (sw), GTK_POLICY_AUTOMATIC, GTK_POLICY_AUTOMATIC);
	gtk_scrolled_window_set_shadow_type (GTK_SCROLLED_WINDOW (sw), GTK_SHADOW_ETCHED_IN);
	gtk_box_pack_start (GTK_BOX(vb2), sw, TRUE, TRUE, 0);

	w_data = gtk_text_view_new ();
	gtk_text_view_set_editable (GTK_TEXT_VIEW (w_data), FALSE);
	gtk_widget_show (w_data);
	gtk_container_add (GTK_CONTAINER (sw), w_data);

	/* buttons */
	hb = gtk_hbox_new (FALSE, 6);
	gtk_widget_show (hb);
	gtk_box_pack_start (GTK_BOX (vb), hb, FALSE, FALSE, 0);

	but = gtk_button_new_with_mnemonic (_("_Content"));
	gtk_widget_show (but);
	gtk_box_pack_start (GTK_BOX (hb), but, FALSE, FALSE, 0);
	g_signal_connect (G_OBJECT (but), "clicked", G_CALLBACK (cb_content),0);

	but = gtk_button_new_with_mnemonic (_("_Styles"));
	gtk_widget_show (but);
	gtk_box_pack_start (GTK_BOX (hb), but, FALSE, FALSE, 0);
	g_signal_connect (G_OBJECT (but), "clicked", G_CALLBACK (cb_styles),0);

	but = gtk_button_new_with_mnemonic (_("_Meta"));
	gtk_widget_show (but);
	gtk_box_pack_start (GTK_BOX (hb), but, FALSE, FALSE, 0);
	g_signal_connect (G_OBJECT (but), "clicked", G_CALLBACK (cb_meta),0);

	but = gtk_button_new_with_mnemonic (_("S_ettings"));
	gtk_widget_show (but);
	gtk_box_pack_start (GTK_BOX (hb), but, FALSE, FALSE, 0);
	g_signal_connect (G_OBJECT (but), "clicked", G_CALLBACK (cb_settings),0);

	gtk_widget_show (win);
}
