/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "internal.h"

static void r_group(ImpRenderCtx *ctx, void *drw_data, iks *node);

struct element_s {
	char *name;
	void (*func)(ImpRenderCtx *ctx, void *drw_data, iks *node);
} elements[] = {
//	{ "draw:image", r_image },
	{ "draw:rect", r_rect },
//	{ "draw:text-box", r_text },
	{ "draw:ellipse", r_circle },
	{ "draw:circle", r_circle },
	{ "draw:line", r_line },
//	{ "draw:connector", r_line },
	{ "draw:polyline", r_polyline },
	{ "draw:polygon", r_polygon },
//	{ "draw:path", r_path },
	{ "draw:g", r_group },
	{ NULL, NULL }
};

ImpRenderCtx *
imp_create_context(const ImpDrawer *drw)
{
	ImpRenderCtx *ctx;

	ctx = calloc(1, sizeof(ImpRenderCtx));
	if (!ctx) return NULL;
	ctx->drw = drw;
	return ctx;
}

void
imp_context_set_page(ImpRenderCtx *ctx, ImpPage *page)
{
	ctx->page = page;
	ctx->content = page->doc->content;
	ctx->styles = page->doc->styles;
}

void
imp_context_set_step(ImpRenderCtx *ctx, int step)
{
	ctx->step = step;
}

static void
find_geometry(ImpRenderCtx *ctx, void *drw_data)
{
	char *tmp;
	iks *x, *y;

	ctx->drw->get_size(drw_data, &ctx->pix_w, &ctx->pix_h);

	tmp = iks_find_attrib(ctx->page->page, "draw:master-page-name");
	x = iks_find(ctx->page->doc->styles, "office:master-styles");
	y = iks_find_with_attrib(x, "style:master-page", "style:name", tmp);
	x = iks_find(ctx->page->doc->styles, "office:automatic-styles");
	y = iks_find_with_attrib(x, "style:page-master", "style:name",
		iks_find_attrib(y, "style:page-master-name"));
	ctx->cm_w = atof(iks_find_attrib(iks_find(y, "style:properties"), "fo:page-width"));
	ctx->cm_h = atof(iks_find_attrib(iks_find(y, "style:properties"), "fo:page-height"));
	ctx->fact_x = ctx->pix_w / ctx->cm_w;
	ctx->fact_y = ctx->pix_h / ctx->cm_h;
}

static void
r_group(ImpRenderCtx *ctx, void *drw_data, iks *node)
{
	iks *x;
	char *element;
	int i;

	for (x = iks_first_tag(node); x; x = iks_next_tag(x)) {
		element = iks_name(x);
		i = 0;
		while (elements[i].name) {
			if (strcmp(element, elements[i].name) == 0) {
				elements[i].func(ctx, drw_data, x);
				break;
			}
			i++;
		}
	}
}

void
imp_render(ImpRenderCtx *ctx, void *drw_data)
{
	iks *x;
	char *element;
	int i;

	find_geometry(ctx, drw_data);

	i = _imp_r_background(ctx, drw_data, ctx->page->page);

	element = iks_find_attrib(ctx->page->page, "draw:master-page-name");
	if (element) {
		x = iks_find_with_attrib(
			iks_find(ctx->page->doc->styles, "office:master-styles"),
			"style:master-page", "style:name", element);
		if (x) {
			if (i == 0) _imp_r_background(ctx, drw_data, x);
			for (x = iks_first_tag(x); x; x = iks_next_tag(x)) {
				if (iks_find_attrib(x, "presentation:class"))
					continue;
				element = iks_name(x);
				i = 0;
				while (elements[i].name) {
					if (strcmp(element, elements[i].name) == 0) {
						elements[i].func(ctx, drw_data, x);
						break;
					}
					i++;
				}
			}
		}
	}

	for (x = iks_first_tag(ctx->page->page); x; x = iks_next_tag(x)) {
		element = iks_name(x);
		i = 0;
		while (elements[i].name) {
			if (strcmp(element, elements[i].name) == 0) {
				elements[i].func(ctx, drw_data, x);
				break;
			}
			i++;
		}
//		printf ("\nUNKNOWN %s\n%s\n\n", iks_name (x), iks_string (iks_stack (x), x));
	}
}

void
imp_delete_context(ImpRenderCtx *ctx)
{
	free(ctx);
}
