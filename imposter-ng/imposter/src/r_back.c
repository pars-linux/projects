/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "internal.h"

int
_imp_r_background(ImpRenderCtx *ctx, void *drw_data, iks *node)
{
/*
	GdkColor col;
	char *type;
	char *stil, *gfx;
	iks *x;

	type = r_get_style (ctx, node, "draw:fill");
	if (!type) return 0;

	if (strcmp (type, "solid") == 0) {
		if (r_get_color (ctx, node, "draw:fill-color", &col)) {
			gdk_gc_set_rgb_fg_color (ctx->gc, &col);
		}
		gdk_draw_rectangle (ctx->d, ctx->gc, TRUE, 0, 0, ctx->pix_w, ctx->pix_h);
	} else if (strcmp (type, "bitmap") == 0) {
		stil = r_get_style (ctx, node, "draw:fill-image-name");
		x = iks_find_with_attrib (iks_find (ctx->styles, "office:styles"),
			"draw:fill-image", "draw:name", stil);
		gfx = iks_find_attrib (x, "xlink:href");
		if (gfx) {
			if (iks_strcmp (r_get_style (ctx, node, "style:repeat"), "stretch") == 0) {
				r_draw_pixbuf (ctx, gfx, 0, 0, ctx->pix_w, ctx->pix_h);
			} else {
				r_tile_pixbuf (ctx, gfx, 0, 0, ctx->pix_w, ctx->pix_h);
			}
		}
	} else if (strcmp (type, "gradient") == 0) {
		r_draw_gradient (ctx, node);
	} else {
		return 0;
	}
	return 1;
*/
}
