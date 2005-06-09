/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "zip.h"

#ifndef INTERNAL_H
#define INTERNAL_H

struct ImpDoc_struct {
	ikstack *stack;
	zip *zfile;
	iks *content;
	iks *styles;
	iks *meta;
	ImpPage *pages;
	ImpPage *last_page;
	int nr_pages;
};

struct ImpPage_struct {
	struct ImpPage_struct *next;
	struct ImpPage_struct *prev;
	ImpDoc *doc;
	iks *page;
	int nr;
};

struct ImpRenderCtx_struct {
	const ImpDrawer *drw;
	ImpPage *page;
	iks *content;
	iks *styles;
	int step;
	int pix_w, pix_h;
	double cm_w, cm_h;
	double fact_x, fact_y;
};

char *r_get_style (ImpRenderCtx *ctx, iks *node, char *attr);
int r_get_color(ImpRenderCtx *ctx, iks *node, char *name, ImpColor *ic);
void r_draw_rect(ImpRenderCtx *ctx, void *drw_data, int fill, int x, int y, int w, int h, int roundness);

int _imp_r_background(ImpRenderCtx *ctx, void *drw_data, iks *node);
void r_polygon(ImpRenderCtx *ctx, void *drw_data, iks *node);
void r_circle(ImpRenderCtx *ctx, void *drw_data, iks *node);
void r_line(ImpRenderCtx *ctx, void *drw_data, iks *node);
void r_rect(ImpRenderCtx *ctx, void *drw_data, iks *node);
void r_polyline(ImpRenderCtx *ctx, void *drw_data, iks *node);
void r_draw_gradient (ImpRenderCtx *ctx, void *drw_data, iks *node);


#endif	/* INTERNAL_H */
