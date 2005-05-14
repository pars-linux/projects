/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen <madcat@e-kolay.net>
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "render_ctx.h"

struct element_s {
	char *name;
	void (*func)(render_ctx *ctx, iks *node);
} elements[] = {
	{ "draw:image", r_image },
	{ "draw:rect", r_rect },
	{ "draw:text-box", r_text },
	{ "draw:ellipse", r_circle },
	{ "draw:circle", r_circle },
	{ "draw:line", r_line },
	{ "draw:connector", r_line },
	{ "draw:polyline", r_polyline },
	{ "draw:polygon", r_polygon },
	{ "draw:path", r_path },
	{ "draw:g", r_group },
	{ NULL, NULL }
};

static void
find_factor (render_ctx *ctx, iks *page)
{
	char *tmp;
	iks *x, *y;

	gdk_drawable_get_size (ctx->d, &ctx->pix_w, &ctx->pix_h);
	tmp = iks_find_attrib (page, "draw:master-page-name");
	x = iks_find (ctx->styles, "office:master-styles");
	y = iks_find_with_attrib (x, "style:master-page", "style:name", tmp);
	x = iks_find (ctx->styles, "office:automatic-styles");
	y = iks_find_with_attrib (x, "style:page-master", "style:name", iks_find_attrib (y, "style:page-master-name"));
	ctx->cm_w = atof (iks_find_attrib (iks_find (y, "style:properties"), "fo:page-width"));
	ctx->cm_h = atof (iks_find_attrib (iks_find (y, "style:properties"), "fo:page-height"));

	ctx->fact_x = ctx->pix_w / ctx->cm_w;
	ctx->fact_y = ctx->pix_h / ctx->cm_h;
}

void
r_group (render_ctx *ctx, iks *node)
{
	iks *x;
	char *element;
	int i;

	for (x = iks_first_tag (node); x; x = iks_next_tag (x)) {
		element = iks_name (x);
		i = 0;
		while (elements[i].name) {
			if (strcmp (element, elements[i].name) == 0) {
				elements[i].func (ctx, x);
				break;
			}
			i++;
		}
	}
}

static int
draw_bg (render_ctx *ctx, iks *node)
{
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
}

void
r_page (render_ctx *ctx, iks *page)
{
	iks *x;
	char *element;
	int i;

	element = iks_find_attrib (page, "draw:id");
	if (element) ctx->page_no = atoi (element);

	find_factor (ctx, page);

	i = draw_bg (ctx, page);

	element = iks_find_attrib (page, "draw:master-page-name");
	if (element) {
		x = iks_find_with_attrib (iks_find (ctx->styles, "office:master-styles"),
			"style:master-page", "style:name", element);
		if (x) {
			if (i == 0) draw_bg (ctx, x);
			for (x = iks_first_tag (x); x; x = iks_next_tag(x)) {
				if (iks_find_attrib (x, "presentation:class"))
					continue;
				element = iks_name (x);
				i = 0;
				while (elements[i].name) {
					if (strcmp (element, elements[i].name) == 0) {
						elements[i].func (ctx, x);
						break;
					}
					i++;
				}
			}
		}
	}

	for (x = iks_first_tag (page); x; x = iks_next_tag (x)) {
		element = iks_name (x);
		i = 0;
		while (elements[i].name) {
			if (strcmp (element, elements[i].name) == 0) {
				elements[i].func (ctx, x);
				break;
			}
			i++;
		}
//		printf ("\nUNKNOWN %s\n%s\n\n", iks_name (x), iks_string (iks_stack (x), x));
	}
}
