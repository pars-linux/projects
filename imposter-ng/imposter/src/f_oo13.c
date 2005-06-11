/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "internal.h"

//	{ "draw:image", r_image },
//	{ "draw:rect", r_rect },
//	{ "draw:text-box", r_text },
//	{ "draw:ellipse", r_circle },
//	{ "draw:circle", r_circle },
//	{ "draw:line", r_line },
//	{ "draw:connector", r_line },
//	{ "draw:polyline", r_polyline },
//	{ "draw:polygon", r_polygon },
//	{ "draw:path", r_path },
//	{ "draw:g", r_group },

static void
render_object(ImpRenderCtx *ctx, void *drw_data, iks *x)
{
	char *tag, *t;
	ImpColor fg;

	tag = iks_name(x);
	if (strcmp(tag, "draw:g") == 0) {
		iks *y;
		for (y = iks_first_tag(x); y; y = iks_next_tag(y)) {
			render_object(ctx, drw_data, y);
		}
	} else if (strcmp(tag, "draw:line") == 0) {
		r_get_color(ctx, x, "svg:stroke-color", &fg);
		ctx->drw->set_fg_color(drw_data, &fg);
		ctx->drw->draw_line(drw_data,
			r_get_x(ctx, x, "svg:x1"), r_get_y(ctx, x, "svg:y1"),
			r_get_x(ctx, x, "svg:x2"), r_get_y(ctx, x, "svg:y2")
		);
	} else if (strcmp(tag, "draw:rect") == 0) {
		struct ImpRect rect;
		r_get_color(ctx, x, "svg:stroke-color", &rect.fg);
		r_get_color(ctx, x, "draw:fill-color", &rect.bg);
		rect.x = r_get_x(ctx, x, "svg:x");
		rect.y = r_get_y(ctx, x, "svg:y");
		rect.w = r_get_x(ctx, x, "svg:width");
		rect.h = r_get_y(ctx, x, "svg:height");
		t = r_get_style(ctx, x, "draw:corner-radius");
		rect.round = 0;
		if (t) rect.round = atof(t) * ctx->fact_x;
		t = r_get_style(ctx, x, "draw:fill");
		if (t) rect.fill = 1; else rect.fill = 0;
		_imp_r_rect(ctx, drw_data, &rect);
	} else if (strcmp(tag, "draw:ellipse") == 0 || strcmp(tag, "draw:circle") == 0) {
		int sa, ea, fill = 0;
		r_get_color(ctx, x, "svg:stroke-color", &fg);
		sa = r_get_angle(x, "draw:start-angle", 0);
		ea = r_get_angle(x, "draw:end-angle", 360);
		if (ea > sa) ea = ea - sa; else ea = 360 + ea - sa;
		t = r_get_style(ctx, x, "draw:fill");
		if (t) fill = 1;
		ctx->drw->set_fg_color(drw_data, &fg);
		ctx->drw->draw_arc(drw_data,
			fill,
			r_get_x(ctx, x, "svg:x"), r_get_y(ctx, x, "svg:y"),
			r_get_x(ctx, x, "svg:width"), r_get_y(ctx, x, "svg:height"),
			sa, ea
		);
	} else {
		printf("Unknown element: %s\n", tag);
	}
}

static void
render_page(ImpRenderCtx *ctx, void *drw_data)
{
	iks *x;

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
	for (x = iks_first_tag(ctx->page->page); x; x = iks_next_tag(x)) {
		render_object(ctx, drw_data, x);
	}
}

static void
get_geometry(ImpRenderCtx *ctx)
{
	char *tmp;
	iks *x, *y;

	tmp = iks_find_attrib(ctx->page->page, "draw:master-page-name");
	x = iks_find(ctx->page->doc->styles, "office:master-styles");
	y = iks_find_with_attrib(x, "style:master-page", "style:name", tmp);
	x = iks_find(ctx->page->doc->styles, "office:automatic-styles");
	y = iks_find_with_attrib(x, "style:page-master", "style:name",
		iks_find_attrib(y, "style:page-master-name"));
	ctx->cm_w = atof(iks_find_attrib(iks_find(y, "style:properties"), "fo:page-width"));
	ctx->cm_h = atof(iks_find_attrib(iks_find(y, "style:properties"), "fo:page-height"));
}

int
_imp_oo13_load(ImpDoc *doc)
{
	ImpPage *page;
	char *class;
	iks *x;
	int i;

	class = iks_find_attrib(doc->content, "office:class");
	if (iks_strcmp(class, "presentation") != 0) return IMP_NOTIMP;

	x = iks_find(iks_find(doc->content, "office:body"), "draw:page");
	if (!x) return IMP_NOTIMP;
	i = 0;
	for (; x; x = iks_next_tag(x)) {
		if (strcmp(iks_name(x), "draw:page") == 0) {
			page = iks_stack_alloc(doc->stack, sizeof(ImpPage));
			if (!page) return IMP_NOMEM;
			memset(page, 0, sizeof(ImpPage));
			page->page = x;
			page->nr = ++i;
			page->name = iks_find_attrib(x, "draw:name");
			page->doc = doc;
			if (!doc->pages) doc->pages = page;
			page->prev = doc->last_page;
			if (doc->last_page) doc->last_page->next = page;
			doc->last_page = page;
		}
	}
	doc->nr_pages = i;
	doc->get_geometry = get_geometry;
	doc->render_page = render_page;

	return 0;
}
