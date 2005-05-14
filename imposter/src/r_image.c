/* imposter (OO.org Impress viewer)
** Copyright (C) 2003 Gurer Ozen <madcat@e-kolay.net>
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "render_ctx.h"

void
r_image (render_ctx *ctx, iks *node)
{
	GdkPixbuf *orig_pb, *pb;
	char *name;
	int x, y, w, h;

	name = iks_find_attrib (node, "xlink:href");
	if (!name) return;
	name++;
	x = r_get_x (ctx, node, "svg:x");
	y = r_get_y (ctx, node, "svg:y");
	w = r_get_x (ctx, node, "svg:width");
	h = r_get_y (ctx, node, "svg:height");

	orig_pb = oo_doc_get_gfx (ctx->doc, name);

	pb = gdk_pixbuf_scale_simple (orig_pb, w, h, GDK_INTERP_BILINEAR);
	gdk_draw_pixbuf (ctx->d, ctx->gc, pb, 0, 0, x, y, w, h, GDK_RGB_DITHER_NONE, 0, 0);
	g_object_unref (pb);
}
