/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "internal.h"

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
	// find drawing area size
	ctx->drw->get_size(drw_data, &ctx->pix_w, &ctx->pix_h);
	// find page size
	ctx->page->doc->get_geometry(ctx);
	// calculate ratio
	ctx->fact_x = ctx->pix_w / ctx->cm_w;
	ctx->fact_y = ctx->pix_h / ctx->cm_h;
}

void
imp_render(ImpRenderCtx *ctx, void *drw_data)
{
	struct ImpElement elm;

	find_geometry(ctx, drw_data);
/*
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
*/
	while (1) {
		ctx->page->doc->get_next_element(ctx, &elm);
		switch (elm.type) {
			case IMP_ELM_LINE:
				ctx->drw->set_fg_color(drw_data, &elm.line.fg);
				ctx->drw->draw_line(drw_data,
					elm.line.x1, elm.line.y1,
					elm.line.x2, elm.line.y2
				);
				break;
			case IMP_ELM_RECT:
				_imp_r_rect(ctx, drw_data, &elm.rect);
				break;
			case IMP_ELM_CIRCLE:
				ctx->drw->set_fg_color(drw_data, &elm.circle.fg);
				ctx->drw->draw_arc(drw_data,
					elm.circle.fill,
					elm.circle.x, elm.circle.y, elm.circle.w, elm.circle.h,
					elm.circle.sa, elm.circle.ea
				);
				break;
			case IMP_ELM_END:
				return;
		}
	}
}

void
imp_delete_context(ImpRenderCtx *ctx)
{
	free(ctx);
}
