/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "internal.h"
#include <math.h>
/*
void
r_draw_pixbuf (render_ctx *ctx, char *name, int x, int y, int w, int h)
{
	GdkPixbuf *orig_pb, *pb;

	if (name[0] == '#') name++;

	orig_pb = oo_doc_get_gfx (ctx->doc, name);
	pb = gdk_pixbuf_scale_simple (orig_pb, w, h, GDK_INTERP_BILINEAR);
	gdk_draw_pixbuf (ctx->d, ctx->gc, pb, 0, 0, ctx->start_x + x, ctx->start_y + y, w, h, GDK_RGB_DITHER_NONE, 0, 0);
	g_object_unref (pb);
}

void
r_tile_pixbuf (render_ctx *ctx, char *name, int x, int y, int w, int h)
{
	GdkPixbuf *orig_pb, *pb;
	int gw, gh;
	int gx, gy;

	if (name[0] == '#') name++;

	orig_pb = oo_doc_get_gfx (ctx->doc, name);
	gw = gdk_pixbuf_get_width (orig_pb);
	gh = gdk_pixbuf_get_height (orig_pb);
	pb = orig_pb;
//	pb = gdk_pixbuf_scale_simple (orig_pb, gw, gh, GDK_INTERP_BILINEAR);

	for (gx = x; gx < w; gx += gw) {
		for (gy = y; gy < h; gy += gh) {
			gdk_draw_pixbuf (ctx->d, ctx->gc, pb, 0, 0,
				ctx->start_x + gx, ctx->start_y + gy, gw, gh, GDK_RGB_DITHER_NONE, 0, 0);
		}
	}

//	g_object_unref (pb);
}
*/

void
r_draw_rect(ImpRenderCtx *ctx, void *drw_data, int fill, int x, int y, int w, int h, int roundness)
{
	int a;

	if (0 == roundness) {
		ctx->drw->draw_rect(drw_data, fill, x, y, w, h);
		return;
	}

	ctx->drw->draw_arc(drw_data, fill,
		x, y, roundness, roundness, 90, 90);
	ctx->drw->draw_arc(drw_data, fill,
		x + w - roundness, y, roundness, roundness, 0, 90);
	ctx->drw->draw_arc(drw_data, fill,
		x + w - roundness, y + h - roundness, roundness, roundness, 270, 90);
	ctx->drw->draw_arc(drw_data, fill,
		x, y + h - roundness, roundness, roundness, 180, 90);

	a = roundness / 2;
	if (fill) {
		ctx->drw->draw_rect(drw_data, 1, x + a, y, w - a - a, h);
		ctx->drw->draw_rect(drw_data, 1, x, y + a, w, h - a - a);
		return;
	}
	ctx->drw->draw_line(drw_data, x + a, y, x + w - a, y);
	ctx->drw->draw_line(drw_data, x + a, y + h, x + w - a, y + h);
	ctx->drw->draw_line(drw_data, x, y + a, x, y + h - a);
	ctx->drw->draw_line(drw_data, x + w, y + a, x + w, y + h - a);
}
