/* imposter (OO.org Impress viewer)
** Copyright (C) 2003 Gurer Ozen <madcat@e-kolay.net>
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"

struct fcache {
	char *name;
	iks *x;
	GdkPixbuf *pb;
};

enum {
	OPEN_SIGNAL,
	CLOSE_SIGNAL,
	NR_SIGNALS
};

static guint oo_doc_sigs[NR_SIGNALS] = { 0, 0 };

static void
page_parse (OODoc *obj)
{
	iks *x;
	struct page_s *pg;
	int i = 0;

	x = iks_find (iks_find (obj->content, "office:body"), "draw:page");
	while (x) {
		if (strcmp (iks_name (x), "draw:page") == 0) {
			pg = malloc (sizeof (struct page_s));
			memset (pg, 0, sizeof (struct page_s));
			pg->node = x;
			pg->name = iks_find_attrib (x, "draw:name");
			pg->nr = ++i;
			obj->pages = g_list_append (obj->pages, pg);
		}
		x = iks_next_tag (x);
	}
}

static void
oo_doc_class_init (OODocClass *class)
{
	oo_doc_sigs[OPEN_SIGNAL] =
		g_signal_new ("doc-open", OO_TYPE_DOC,
			G_SIGNAL_RUN_FIRST, G_STRUCT_OFFSET (OODocClass, doc_open),
			NULL, NULL,
			g_cclosure_marshal_VOID__VOID,
			G_TYPE_NONE, 0);

	oo_doc_sigs[CLOSE_SIGNAL] =
		g_signal_new ("doc-close", OO_TYPE_DOC,
			G_SIGNAL_RUN_FIRST, G_STRUCT_OFFSET (OODocClass, doc_close),
			NULL, NULL,
			g_cclosure_marshal_VOID__VOID,
			G_TYPE_NONE, 0);

	class->doc_open = NULL;
	class->doc_close = NULL;
}

static void
oo_doc_init (OODoc *obj)
{
	obj->flags = 0;
	obj->filename = NULL;
	obj->file = NULL;
	obj->file_cache = g_hash_table_new (g_str_hash, g_str_equal);
	obj->pages = NULL;
}

GType
oo_doc_get_type (void)
{
	static GType oo_doc_type = 0;

	if (!oo_doc_type) {
		static const GTypeInfo oo_doc_info = {
			sizeof (OODocClass),
			NULL,
			NULL,
			(GClassInitFunc) oo_doc_class_init,
			NULL,
			NULL,
			sizeof (OODoc),
			0,
			(GInstanceInitFunc) oo_doc_init
		};
		oo_doc_type = g_type_register_static (G_TYPE_OBJECT, "OODoc", &oo_doc_info, 0);
	}
	return oo_doc_type;
}

GObject *
oo_doc_new (void)
{
	return G_OBJECT (g_object_new (oo_doc_get_type (), NULL));
}

gboolean
oo_doc_open (OODoc *obj, const char *filename, GError **err)
{
	char *class;
	int e;

	if (obj->flags & OO_DOC_HAS_FILE) oo_doc_close (obj);

	obj->filename = g_strdup (filename);

	obj->file =  zip_open (filename, &e);
	if (e) {
		g_set_error (err, 0, 0, _("%s"), zip_error (e));
		oo_doc_close (obj);
		return FALSE;
	}

	obj->content = oo_doc_get_xml (obj, "content.xml");
	obj->styles = oo_doc_get_xml (obj, "styles.xml");
	obj->meta = oo_doc_get_xml (obj, "meta.xml");

	if (!obj->content || !obj->styles) {
		g_set_error (err, 0, 0, _("Cannot find content"));
		oo_doc_close (obj);
		return FALSE;
	}

	class = iks_find_attrib (obj->content, "office:class");
	if (iks_strcmp (class, "presentation") != 0) {
		g_set_error (err, 0, 0, _("Not a presentation file"));
		oo_doc_close (obj);
		return FALSE;
	}

	page_parse (obj);

	obj->flags |= OO_DOC_HAS_FILE;
	g_signal_emit (G_OBJECT (obj), oo_doc_sigs[OPEN_SIGNAL], 0);
	return TRUE;
}

static gboolean
free_cached_file (char *key, struct fcache *fc, gpointer data)
{
	free (fc->name);
	if (fc->x) iks_delete (fc->x);
	if (fc->pb) g_object_unref (G_OBJECT (fc->pb));
	free (fc);
	return TRUE;
}

void
oo_doc_close (OODoc *obj)
{
	if (obj->flags & OO_DOC_HAS_FILE)
		g_signal_emit (G_OBJECT (obj), oo_doc_sigs[CLOSE_SIGNAL], 0);

	if (obj->filename) free (obj->filename);
	obj->filename = NULL;

	if (obj->file) zip_close (obj->file);
	obj->file = NULL;

	g_hash_table_foreach_remove (obj->file_cache, (GHRFunc)free_cached_file, NULL);

	obj->pages = NULL;

	obj->flags = 0;
}

int
oo_doc_has_file (OODoc *obj)
{
	if (obj->flags & OO_DOC_HAS_FILE) return 1;
	return 0;
}

GList *
oo_doc_get_page_list (OODoc *obj)
{
	return obj->pages;
}

char *
oo_doc_get_filename (OODoc *obj)
{
	return obj->filename;
}

GdkPixbuf *
oo_doc_get_gfx (OODoc *obj, const char *gfxfile)
{
	struct fcache *fc;
	GdkPixbufLoader *gpl;
	char *pix;
	size_t len;
//	int err;

	fc = g_hash_table_lookup (obj->file_cache, gfxfile);
	if (fc) return fc->pb;

	len = zip_get_size (obj->file, gfxfile);
	pix = malloc (len);
	if (!pix) return NULL;

	zip_load (obj->file, gfxfile, pix);
	gpl = gdk_pixbuf_loader_new ();
	gdk_pixbuf_loader_write (gpl, pix, len, NULL);

	fc = malloc (sizeof (struct fcache));
	fc->name = g_strdup (gfxfile);
	fc->x = NULL;

	gdk_pixbuf_loader_close (gpl, NULL);
	free (pix);
	fc->pb = gdk_pixbuf_loader_get_pixbuf (gpl);

	g_hash_table_insert (obj->file_cache, fc->name, fc);
	return fc->pb;
}

iks *
oo_doc_get_xml (OODoc *obj, const char *xmlfile)
{
	int err;
	struct fcache *fc;

	fc = g_hash_table_lookup (obj->file_cache, xmlfile);
	if (fc) return fc->x;

	fc = malloc (sizeof (struct fcache));
	fc->name = g_strdup (xmlfile);
	fc->pb = NULL;
	fc->x = zip_load_xml (obj->file, xmlfile, &err);
// FIXME
	if (err) {
		return NULL;
	}

	g_hash_table_insert (obj->file_cache, fc->name, fc);
	return fc->x;
}
