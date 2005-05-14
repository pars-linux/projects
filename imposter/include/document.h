/* imposter (OO.org Impress viewer)
** Copyright (C) 2003 Gurer Ozen <madcat@e-kolay.net>
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#ifndef OO_DOC_H
#define OO_DOC_H

#define OO_TYPE_DOC (oo_doc_get_type ())
#define OO_DOC(obj) (G_TYPE_CHECK_INSTANCE_CAST ((obj), OO_TYPE_DOC , OODoc))
#define OO_DOC_CLASS(klass) (G_TYPE_CHECK_CLASS_CAST ((klass), OO_TYPE_DOC , OODocClass))

typedef struct _OODoc OODoc;
typedef struct _OODocClass OODocClass;

struct page_s {
	iks *node;
	char *name;
	int nr;
};

#define OO_DOC_HAS_FILE 1

struct _OODoc {
	GObject instance;
	char *filename;
	int flags;
	zip *file;
	GList *pages;
	GHashTable *file_cache;
	iks *meta;
	iks *content;
	iks *styles;
};

struct _OODocClass {
	GObjectClass parent_class;
	void (*doc_open)(OODoc *obj);
	void (*doc_close)(OODoc *obj);
};

GType oo_doc_get_type (void);
GObject *oo_doc_new (void);
gboolean oo_doc_open (OODoc *obj, const char *filename, GError **err);
void oo_doc_close (OODoc *obj);
int oo_doc_has_file (OODoc *obj);
GList *oo_doc_get_page_list (OODoc *obj);
char *oo_doc_get_filename (OODoc *obj);
GdkPixbuf *oo_doc_get_gfx (OODoc *obj, const char *gfxfile);
iks *oo_doc_get_xml (OODoc *obj, const char *xmlfile);



#endif	/* OO_DOC_H */
