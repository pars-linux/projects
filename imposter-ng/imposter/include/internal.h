/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "zip.h"

#ifndef INTERNAL_H
#define INTERNAL_H

enum {
	IMP_ELM_LINE,
	IMP_ELM_RECT,
	IMP_ELM_CIRCLE,
	IMP_ELM_END
};

struct ImpElement {
	int type;
	union {
		struct ImpRect {
			int fill;
			int x, y;
			int w, h;
			int round;
			ImpColor fg;
			ImpColor bg;
		} rect ;
		struct ImpCircle {
			int fill;
			int x, y;
			int w, h;
			int sa, ea;
			ImpColor fg;
		} circle;
		struct ImpLine {
			ImpColor fg;
			int x1, y1;
			int x2, y2;
		} line;
	};
};

struct ImpDoc_struct {
	ikstack *stack;
	zip *zfile;
	iks *content;
	iks *styles;
	iks *meta;
	ImpPage *pages;
	ImpPage *last_page;
	int nr_pages;
	void (*get_geometry)(ImpRenderCtx *ctx);
	void (*get_next_element)(ImpRenderCtx *ctx, struct ImpElement *elm);
};

struct ImpPage_struct {
	struct ImpPage_struct *next;
	struct ImpPage_struct *prev;
	ImpDoc *doc;
	iks *page;
	const char *name;
	int nr;
};

struct ImpRenderCtx_struct {
	const ImpDrawer *drw;
	ImpPage *page;
	iks *content;
	iks *styles;
	iks *last_element;
	int step;
	int pix_w, pix_h;
	double cm_w, cm_h;
	double fact_x, fact_y;
};

char *r_get_style (ImpRenderCtx *ctx, iks *node, char *attr);
int r_get_color(ImpRenderCtx *ctx, iks *node, char *name, ImpColor *ic);
void r_parse_color(const char *color, ImpColor *ic);
void r_draw_rect(ImpRenderCtx *ctx, void *drw_data, int fill, int x, int y, int w, int h, int roundness);
int r_get_x (ImpRenderCtx *ctx, iks *node, char *name);
int r_get_y (ImpRenderCtx *ctx, iks *node, char *name);
int r_get_angle (iks *node, char *name, int def);

void _imp_r_rect(ImpRenderCtx *ctx, void *drw_data, struct ImpRect *rect);

int _imp_r_background(ImpRenderCtx *ctx, void *drw_data, iks *node);
void r_polygon(ImpRenderCtx *ctx, void *drw_data, iks *node);
void r_circle(ImpRenderCtx *ctx, void *drw_data, iks *node);
void r_line(ImpRenderCtx *ctx, void *drw_data, iks *node);
void r_polyline(ImpRenderCtx *ctx, void *drw_data, iks *node);
void r_draw_gradient (ImpRenderCtx *ctx, void *drw_data, iks *node);

int _imp_oo13_load(ImpDoc *doc);
int _imp_oasis_load(ImpDoc *doc);


#endif	/* INTERNAL_H */
