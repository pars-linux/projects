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
get_next_element(ImpRenderCtx *ctx, struct ImpElement *elm)
{
	iks *x;
	char *tag, *t;

	x = ctx->last_element;
	if (x) {
		x = iks_next_tag(x);
	} else {
		x = iks_first_tag(ctx->page->page);
	}
	for (; x; x = iks_next_tag(x)) {
		tag = iks_name(x);
		if (strcmp(tag, "draw:line") == 0) {
			r_get_color(ctx, x, "svg:stroke-color", &elm->line.fg);
			elm->type = IMP_ELM_LINE;
			elm->line.x1 = r_get_x(ctx, x, "svg:x1");
			elm->line.y1 = r_get_y(ctx, x, "svg:y1");
			elm->line.x2 = r_get_x(ctx, x, "svg:x2");
			elm->line.y2 = r_get_y(ctx, x, "svg:y2");
			break;
		} else if (strcmp(tag, "draw:rect") == 0) {
			r_get_color(ctx, x, "svg:stroke-color", &elm->rect.fg);
			r_get_color(ctx, x, "draw:fill-color", &elm->rect.bg);
			elm->type = IMP_ELM_RECT;
			elm->rect.x = r_get_x(ctx, x, "svg:x");
			elm->rect.y = r_get_y(ctx, x, "svg:y");
			elm->rect.w = r_get_x(ctx, x, "svg:width");
			elm->rect.h = r_get_y(ctx, x, "svg:height");
			t = r_get_style(ctx, x, "draw:corner-radius");
			elm->rect.round = 0;
			if (t) elm->rect.round = atof(t) * ctx->fact_x;
			t = r_get_style(ctx, x, "draw:fill");
			if (t) elm->rect.fill = 1; else elm->rect.fill = 0;
			break;
		} else if (strcmp(tag, "ellipse") == 0 || strcmp(tag, "circle") == 0) {
			r_get_color(ctx, x, "svg:stroke-color", &elm->circle.fg);
			elm->type = IMP_ELM_CIRCLE;
			elm->circle.x = r_get_x(ctx, x, "svg:x");
			elm->circle.y = r_get_y(ctx, x, "svg:y");
			elm->circle.w = r_get_x(ctx, x, "svg:width");
			elm->circle.h = r_get_y(ctx, x, "svg:height");
			elm->circle.sa = r_get_angle(x, "draw:start-angle", 0);
			elm->circle.ea = r_get_angle(x, "draw:end-angle", 360);
			if (elm->circle.ea > elm->circle.sa) {
				elm->circle.ea = elm->circle.ea - elm->circle.sa;
			} else {
				elm->circle.ea = 360 + elm->circle.ea - elm->circle.sa;
			}
			t = r_get_style(ctx, x, "draw:fill");
			if (t) elm->circle.fill = 1; else elm->circle.fill = 0;
			break;
		} else {
			printf("Unknown element: %s\n", tag);
		}
	}
	if (!x) elm->type = IMP_ELM_END;
	ctx->last_element = x;
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
	doc->get_next_element = get_next_element;

	return 0;
}
