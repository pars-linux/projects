/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2004 Gurer Ozen <madcat@e-kolay.net>
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "render.h"
#include "render_ctx.h"

enum {
	PAGE_SIGNAL,
	NR_SIGNALS
};

static guint render_sigs[NR_SIGNALS] = { 0 };

static gboolean
cb_expose (GtkWidget *w, GdkEventExpose *ev, gpointer data)
{
	OORender *obj = OO_RENDER (w);

	if (obj->doc && obj->page) {
		render_ctx ctx;

		memset (&ctx, 0, sizeof (ctx));
		ctx.pango_ctx = gtk_widget_get_pango_context (w);
		ctx.d = w->window;
		ctx.doc = obj->doc;
		ctx.step = obj->step;
		ctx.step_mode = obj->step_mode;
		ctx.content = oo_doc_get_xml (obj->doc, "content.xml");
		ctx.styles = oo_doc_get_xml (obj->doc, "styles.xml");
		ctx.gc = gdk_gc_new (w->window);
		r_page (&ctx, ((struct page_s *)obj->page->data)->node);
		g_object_unref (ctx.gc);
	}
	return TRUE;
}

static void
render_class_init (OORenderClass *class)
{
	render_sigs[PAGE_SIGNAL] =
		g_signal_new ("page-changed", OO_TYPE_RENDER,
			G_SIGNAL_RUN_FIRST, G_STRUCT_OFFSET (OORenderClass, page_changed),
			NULL, NULL,
			g_cclosure_marshal_VOID__POINTER,
			G_TYPE_NONE, 1, G_TYPE_POINTER);

	class->page_changed = NULL;
}

static void
render_init (OORender *obj)
{
	obj->doc = NULL;
	obj->page = NULL;
	obj->step = 0;
	obj->step_mode = 0;
	g_signal_connect (G_OBJECT (obj), "expose_event", G_CALLBACK (cb_expose), NULL);
}

GType
oo_render_get_type (void)
{
	static GType render_type = 0;

	if (!render_type) {
		static const GTypeInfo render_info = {
			sizeof (OORenderClass),
			NULL,
			NULL,
			(GClassInitFunc) render_class_init,
			NULL,
			NULL,
			sizeof (OORender),
			0,
			(GInstanceInitFunc) render_init
		};
		render_type = g_type_register_static (GTK_TYPE_DRAWING_AREA, "Render", &render_info, 0);
	}
	return render_type;
}

GtkWidget *
oo_render_new (void)
{
	return GTK_WIDGET (g_object_new (oo_render_get_type (), NULL));
}

static void
render_update (GObject *w, OORender *obj)
{
	if (obj->doc && oo_doc_has_file (obj->doc)) {
		oo_render_set_page (obj, g_list_first (oo_doc_get_page_list (obj->doc)));
	} else {
		gtk_widget_queue_draw (GTK_WIDGET (obj));
	}
}

static void
render_clean (GObject *w, OORender *obj)
{
	obj->page = NULL;
	gtk_widget_queue_draw (GTK_WIDGET (obj));
}

void
oo_render_set_document (OORender *obj, OODoc *doc)
{
	obj->doc = doc;
	g_signal_connect (G_OBJECT (doc), "doc-open", G_CALLBACK (render_update), obj);
	g_signal_connect (G_OBJECT (doc), "doc-close", G_CALLBACK (render_clean), obj);
}

void
oo_render_set_page (OORender *obj, GList *page)
{
	if (page == obj->page) return;
	obj->page = page;
	obj->step = 0;
	gtk_widget_queue_draw (GTK_WIDGET (obj));
	gtk_signal_emit (GTK_OBJECT (obj), render_sigs[PAGE_SIGNAL], obj->page->data);
}

GList *
oo_render_get_page (OORender *obj)
{
	return obj->page;
}

void
oo_render_step (OORender *obj)
{
	obj->step++;
	gtk_widget_queue_draw (GTK_WIDGET (obj));
}

void
oo_render_step_mode (OORender *obj, int mode)
{
	obj->step = 0;
	obj->step_mode = mode;
	gtk_widget_queue_draw (GTK_WIDGET (obj));
}
