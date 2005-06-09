/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "internal.h"

iks *
_imp_load_xml(ImpDoc *doc, const char *xmlfile)
{
	int e;
	iks *x;

	x = zip_load_xml (doc->zfile, xmlfile, &e);
	return x;
}

ImpDoc *
imp_open(const char *filename, int *err)
{
	ImpDoc *doc;
	ImpPage *page;
	const char *class;
	int e, i;
	iks *x;

	doc = calloc(1, sizeof(ImpDoc));
	if (!doc) {
		*err = IMP_NOMEM;
		return NULL;
	}

	doc->stack = iks_stack_new(sizeof(ImpPage) * 32, 0);
	if (!doc->stack) {
		*err = IMP_NOMEM;
		imp_close(doc);
		return NULL;
	}

	doc->zfile = zip_open(filename, &e);
	if (e) {
		*err = IMP_NOTZIP;
		imp_close(doc);
		return NULL;
	}

	doc->content = _imp_load_xml(doc, "content.xml");
	doc->styles = _imp_load_xml(doc, "styles.xml");
	doc->meta = _imp_load_xml(doc, "meta.xml");

	if (!doc->content || !doc->styles) {
		*err = IMP_BADDOC;
		imp_close(doc);
		return NULL;
	}

	class = iks_find_attrib(doc->content, "office:class");
	if (iks_strcmp(class, "presentation") != 0) {
		*err = IMP_NOTIMP;
		imp_close(doc);
		return NULL;
	}

	x = iks_find(iks_find(doc->content, "office:body"), "draw:page");
	i = 0;
	for (; x; x = iks_next_tag(x)) {
		if (strcmp(iks_name(x), "draw:page") == 0) {
			page = iks_stack_alloc(doc->stack, sizeof(ImpPage));
			if (!page) {
				*err = IMP_NOMEM;
				imp_close(doc);
				return NULL;
			}
			memset(page, 0, sizeof(ImpPage));
			page->page = x;
			page->nr = ++i;
			page->doc = doc;
			if (!doc->pages) doc->pages = page;
			page->prev = doc->last_page;
			if (doc->last_page) doc->last_page->next = page;
			doc->last_page = page;
		}
	}
	doc->nr_pages = i;

	return doc;
}

int
imp_nr_pages(ImpDoc *doc)
{
	return doc->nr_pages;
}

ImpPage *
imp_get_page(ImpDoc *doc, int page_no)
{
	if (page_no == IMP_LAST_PAGE) {
		return doc->last_page;
	} else {
		ImpPage *page;
		if (page_no < 0 || page_no > doc->nr_pages) return NULL;
		for (page = doc->pages; page_no; --page_no) {
			page = page->next;
		}
		return page;
	}
}

ImpPage *
imp_next_page(ImpPage *page)
{
	return page->next;
}

ImpPage *
imp_prev_page(ImpPage *page)
{
	return page->prev;
}

int
imp_get_page_no(ImpPage *page)
{
	return page->nr;
}

const char *
imp_get_page_name(ImpPage *page)
{
	return iks_find_attrib(page->page, "draw:name");
}

void
imp_close(ImpDoc *doc)
{
	if (doc->stack) iks_stack_delete(doc->stack);
	if (doc->zfile) zip_close(doc->zfile);
	free(doc);
}
