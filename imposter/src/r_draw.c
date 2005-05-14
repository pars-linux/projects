/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2004 Gurer Ozen <madcat@e-kolay.net>
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "render_ctx.h"

#include <math.h>

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

void
r_draw_move (render_ctx *ctx, int x, int y)
{
	ctx->pen_x = x;
	ctx->pen_y = y;
}

void
r_draw_lineto (render_ctx *ctx, int x, int y)
{
	gdk_draw_line (ctx->d, ctx->gc,
		ctx->start_x + ctx->pen_x, ctx->start_y + ctx->pen_y,
		ctx->start_x + x, ctx->start_y + y);
	ctx->pen_x = x;
	ctx->pen_y = y;
}

void
r_draw_curveto (render_ctx *ctx, int x, int y, int c1x, int c1y, int c2x, int c2y)
{
	draw_bezier (ctx->d, ctx->gc,
		ctx->start_x + ctx->pen_x, ctx->start_y + ctx->pen_y,
		ctx->start_x + c1x, ctx->start_y + c1y,
		ctx->start_x + c2x, ctx->start_y + c2y,
		ctx->start_x + x, ctx->start_y + y);
	ctx->pen_x = x;
	ctx->pen_y = y;
}

void
r_draw_rect (render_ctx *ctx, gboolean fill, int x, int y, int w, int h, int roundness)
{
	int a;

	if (0 == roundness) {
		gdk_draw_rectangle (ctx->d, ctx->gc, fill,
			ctx->start_x + x, ctx->start_y + y,
			w, h);
		return;
	}
	gdk_draw_arc (ctx->d, ctx->gc, fill,
		ctx->start_x + x, ctx->start_y + y,
		roundness, roundness,
		90 * 64, 90 * 64);
	gdk_draw_arc (ctx->d, ctx->gc, fill,
		ctx->start_x + x + w - roundness, ctx->start_y + y,
		roundness, roundness,
		0, 90 * 64);
	gdk_draw_arc (ctx->d, ctx->gc, fill,
		ctx->start_x + x + w - roundness, ctx->start_y + y + h - roundness,
		roundness, roundness,
		270 * 64, 90 * 64);
	gdk_draw_arc (ctx->d, ctx->gc, fill,
		ctx->start_x + x, ctx->start_y + y + h - roundness,
		roundness, roundness,
		180 * 64, 90 * 64);

	a = roundness / 2;
	if (fill) {
		gdk_draw_rectangle (ctx->d, ctx->gc, TRUE,
			ctx->start_x + x + a, ctx->start_y + y,
			w - a -a, h);
		gdk_draw_rectangle (ctx->d, ctx->gc, TRUE,
			ctx->start_x + x, ctx->start_y + y + a,
			w, h - a - a);
		return;
	}
	gdk_draw_line (ctx->d, ctx->gc,
		ctx->start_x + x + a, ctx->start_y + y,
		ctx->start_x + x + w - a, ctx->start_y + y);
	gdk_draw_line (ctx->d, ctx->gc,
		ctx->start_x + x + a, ctx->start_y + y + h,
		ctx->start_x + x + w - a, ctx->start_y + y + h);
	gdk_draw_line (ctx->d, ctx->gc,
		ctx->start_x + x, ctx->start_y + y + a,
		ctx->start_x + x, ctx->start_y + y + h - a);
	gdk_draw_line (ctx->d, ctx->gc,
		ctx->start_x + x + w, ctx->start_y + y + a,
		ctx->start_x + x + w, ctx->start_y + y + h - a);
}
