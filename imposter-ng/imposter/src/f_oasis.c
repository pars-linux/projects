/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "internal.h"

static void
get_next_element(ImpRenderCtx *ctx, struct ImpElement *elm)
{
	elm->type = IMP_ELM_END;
}

static void
get_geometry(ImpRenderCtx *ctx)
{
}

int
_imp_oasis_load(ImpDoc *doc)
{
	ImpPage *page;
	iks *x, *pres;
	int i;

	pres = iks_find(iks_find(doc->content, "office:body"), "office:presentation");
	if (!pres) return IMP_NOTIMP;

	x = iks_find(pres, "draw:page");
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
