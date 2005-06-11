/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "render.h"

struct my_ctx {
	GdkDrawable *d;
	GdkGC *gc;
	PangoContext *pango_ctx;
};

enum {
	PAGE_SIGNAL,
	NR_SIGNALS
};

static guint render_sigs[NR_SIGNALS] = { 0 };

static void
get_size(void *drw_data, int *w, int *h)
{
	struct my_ctx *ctx = (struct my_ctx *) drw_data;

	gdk_drawable_get_size(ctx->d, w, h);
}

static void
set_fg_color(void *drw_data, ImpColor *color)
{
	struct my_ctx *ctx = (struct my_ctx *) drw_data;
	GdkColor c;

	c.red = color->red;
	c.green = color->green;
	c.blue = color->blue;
	gdk_gc_set_rgb_fg_color(ctx->gc, &c);
}

static void
draw_line(void *drw_data, int x1, int y1, int x2, int y2)
{
	struct my_ctx *ctx = (struct my_ctx *) drw_data;

	gdk_draw_line(ctx->d, ctx->gc, x1, y1, x2, y2);
}

static void
draw_rect(void *drw_data, int fill, int x, int y, int w, int h)
{
	struct my_ctx *ctx = (struct my_ctx *) drw_data;

	gdk_draw_rectangle(ctx->d, ctx->gc, fill, x, y, w, h);
}

static void
draw_polygon(void *drw_data, int fill, ImpPoint *pts, int nr_pts)
{
	struct my_ctx *ctx = (struct my_ctx *) drw_data;

	gdk_draw_polygon(ctx->d, ctx->gc, fill, (GdkPoint *)pts, nr_pts);
}

static void
draw_arc(void *drw_data, int fill, int x, int y, int w, int h, int sa, int ea)
{
	struct my_ctx *ctx = (struct my_ctx *) drw_data;

	gdk_draw_arc(ctx->d, ctx->gc, fill, x, y, w, h, sa * 64, ea * 64);
}

static void
draw_bezier(void *drw_data, int x0, int y0, int x1, int y1, int x2, int y2, int x3, int y3)
{
	struct my_ctx *ctx = (struct my_ctx *) drw_data;

	gtkutil_draw_bezier(ctx->d, ctx->gc, x0, y0, x1, y1, x2, y2, x3, y3);
}

static void *
open_image(void *drw_data, const unsigned char *pix, size_t size)
{
	GdkPixbufLoader *gpl;
	GdkPixbuf *pb;

	gpl = gdk_pixbuf_loader_new();
	gdk_pixbuf_loader_write(gpl, pix, size, NULL);
	gdk_pixbuf_loader_close(gpl, NULL);
	pb = gdk_pixbuf_loader_get_pixbuf(gpl);
	return pb;
}

static void *
scale_image(void *drw_data, void *img_data, int w, int h)
{
	GdkPixbuf *pb = (GdkPixbuf *) img_data;

	return gdk_pixbuf_scale_simple(pb, w, h, GDK_INTERP_BILINEAR);
}

static void
draw_image(void *drw_data, void *img_data, int x, int y, int w, int h)
{
	struct my_ctx *ctx = (struct my_ctx *) drw_data;
	GdkPixbuf *pb = (GdkPixbuf *) img_data;

	gdk_draw_pixbuf(ctx->d, ctx->gc, pb, 0, 0, x, y, w, h, GDK_RGB_DITHER_NONE, 0, 0);
}

static void
close_image(void *drw_data, void *img_data)
{
	GdkPixbuf *pb = (GdkPixbuf *) img_data;

	g_object_unref(G_OBJECT(pb));
}

static const ImpDrawer my_drawer = {
	get_size,
	set_fg_color,
	draw_line,
	draw_rect,
	draw_polygon,
	draw_arc,
	draw_bezier,
	open_image,
	scale_image,
	draw_image,
	close_image
};

static gboolean
cb_expose(GtkWidget *w, GdkEventExpose *ev, gpointer data)
{
	OORender *obj = OO_RENDER (w);

	if (obj->page) {
		struct my_ctx ctx;

		ctx.d = w->window;
		ctx.gc = gdk_gc_new(w->window);
		ctx.pango_ctx = gtk_widget_get_pango_context(w);
		imp_render(obj->ctx, &ctx);
		g_object_unref(ctx.gc);
	}
	return TRUE;
}

static void
render_class_init(OORenderClass *class)
{
	render_sigs[PAGE_SIGNAL] =
		g_signal_new("page-changed", OO_TYPE_RENDER,
			G_SIGNAL_RUN_FIRST, G_STRUCT_OFFSET(OORenderClass, page_changed),
			NULL, NULL,
			g_cclosure_marshal_VOID__POINTER,
			G_TYPE_NONE, 1, G_TYPE_POINTER);

	class->page_changed = NULL;
}

static void
render_init(OORender *obj)
{
	obj->page = NULL;
	obj->ctx = imp_create_context(&my_drawer);
	g_signal_connect(G_OBJECT(obj), "expose_event", G_CALLBACK(cb_expose), NULL);
}

GType
oo_render_get_type(void)
{
	static GType render_type = 0;

	if (!render_type) {
		static const GTypeInfo render_info = {
			sizeof(OORenderClass),
			NULL,
			NULL,
			(GClassInitFunc)render_class_init,
			NULL,
			NULL,
			sizeof(OORender),
			0,
			(GInstanceInitFunc) render_init
		};
		render_type = g_type_register_static(GTK_TYPE_DRAWING_AREA, "Render", &render_info, 0);
	}
	return render_type;
}

GtkWidget *
oo_render_new(void)
{
	return GTK_WIDGET(g_object_new(oo_render_get_type(), NULL));
}

void
oo_render_set_page(OORender *obj, ImpPage *page)
{
	if (page == obj->page) return;
	obj->page = page;
	imp_context_set_page(obj->ctx, page);
	gtk_widget_queue_draw(GTK_WIDGET(obj));
	gtk_signal_emit(GTK_OBJECT(obj), render_sigs[PAGE_SIGNAL], obj->page);
}

ImpPage *
oo_render_get_page(OORender *obj)
{
	return obj->page;
}

void
oo_render_step(OORender *obj)
{
	obj->step++;
	gtk_widget_queue_draw(GTK_WIDGET (obj));
}

void
oo_render_step_mode(OORender *obj, int mode)
{
	obj->step = 0;
	obj->step_mode = mode;
	gtk_widget_queue_draw(GTK_WIDGET (obj));
}
