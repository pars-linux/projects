/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "internal.h"
#include <math.h>

void
_imp_draw_image(ImpRenderCtx *ctx, void *drw_data, const char *name, int x, int y, int w, int h)
{
	void *img1, *img2;
	char *pix;
	size_t len;

	len = zip_get_size(ctx->page->doc->zfile, name);
	pix = malloc(len);
	if (!pix) return;
	zip_load(ctx->page->doc->zfile, name, pix);

	img1 = ctx->drw->open_image(drw_data, pix, len);
	free(pix);
	if (!img1) return;
	img2 = ctx->drw->scale_image(drw_data, img1, w, h);
	if (img2) {
		ctx->drw->draw_image(drw_data, img2, x, y, w, h);
		ctx->drw->close_image(drw_data, img2);
	}
	ctx->drw->close_image(drw_data, img1);
}

/*
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
_imp_draw_rect(ImpRenderCtx *ctx, void *drw_data, int fill, int x, int y, int w, int h, int round)
{
	int a;

	if (0 == round) {
		ctx->drw->draw_rect(drw_data, fill, x, y, w, h);
		return;
	}

	ctx->drw->draw_arc(drw_data, fill,
		x, y, round, round, 90, 90);
	ctx->drw->draw_arc(drw_data, fill,
		x + w - round, y, round, round, 0, 90);
	ctx->drw->draw_arc(drw_data, fill,
		x + w - round, y + h - round, round, round, 270, 90);
	ctx->drw->draw_arc(drw_data, fill,
		x, y + h - round, round, round, 180, 90);

	a = round / 2;
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
