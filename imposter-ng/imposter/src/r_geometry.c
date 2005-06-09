/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "internal.h"
#include <math.h>

int
r_get_color(ImpRenderCtx *ctx, iks *node, char *name, ImpColor *ic)
{
	char *color;
	unsigned int cval;

	color = r_get_style(ctx, node, "draw:fill-color");
	if (!color) return 0;

	if (1 != sscanf(color, "#%X", &cval)) return 0;

	ic->red = (cval & 0xFF0000) >> 8;
	ic->green = cval & 0x00FF00;
	ic->blue = (cval & 0xFF) << 8;

	printf("C %s, %d, %d, %d\n", color,ic->red,ic->green,ic->blue);
	return 1;
}

static void
fg_color(ImpRenderCtx *ctx, void *drw_data, iks *node, char *name)
{
	ImpColor ic;

	if (r_get_color(ctx, node, name, &ic)) {
		ctx->drw->set_fg_color(drw_data, &ic);
	}
}

int
r_get_x (ImpRenderCtx *ctx, iks *node, char *name)
{
	char *val;

	val = iks_find_attrib (node, name);
	if (!val) return 0;
	return atof (val) * ctx->fact_x;
}

int
r_get_y (ImpRenderCtx *ctx, iks *node, char *name)
{
	char *val;

	val = iks_find_attrib (node, name);
	if (!val) return 0;
	return atof (val) * ctx->fact_y;
}

static int
r_get_angle (iks *node, char *name, int def)
{
	char *tmp;

	tmp = iks_find_attrib (node, name);
	if (!tmp) return def;
	return atof (tmp);
}

void
r_circle(ImpRenderCtx *ctx, void *drw_data, iks *node)
{
	int x, y, w, h, sa, ea;
	int fill = 1;
	char *tmp;

	x = r_get_x (ctx, node, "svg:x");
	y = r_get_y (ctx, node, "svg:y");
	w = r_get_x (ctx, node, "svg:width");
	h = r_get_y (ctx, node, "svg:height");
	sa = r_get_angle (node, "draw:start-angle", 0);
	ea = r_get_angle (node, "draw:end-angle", 360);
	if (ea > sa)
		ea = ea - sa;
	else
		ea = 360 + ea - sa;

	tmp = r_get_style (ctx, node, "draw:fill");
	if (!tmp || strcmp (tmp, "solid") != 0) fill = 0;

	tmp = iks_find_attrib (node, "draw:kind");
	if (iks_strcmp (tmp, "arc") == 0) fill = 0;

	ctx->drw->draw_arc(drw_data, fill, x, y, w, h, sa, ea);
}

void
r_arrow (ImpRenderCtx *ctx, void *drw_data, iks *node, int x, int y, int x2, int y2)
{
	ImpPoint pts[4];
	double ia, a;

	pts[0].x = x2;
	pts[0].y = y2;

	ia = 20 * 3.14 * 2 / 360;

	if (x2-x == 0) {
		if (y < y2) a = 3.14 + (3.14 / 2); else a = (3.14 / 2);
	} else if (y2-y == 0) {
		if (x < x2) a = 3.14; else a = 0;
	} else
		a = atan ((y2-y) / (x2-x)) - 3.14;

	pts[1].x = x2 + 0.3 * ctx->fact_x * cos (a - ia);
	pts[1].y = y2 + 0.3 * ctx->fact_y * sin (a - ia);

	pts[2].x = x2 + 0.3 * ctx->fact_x * cos (a + ia);
	pts[2].y = y2 + 0.3 * ctx->fact_y * sin (a + ia);

	ctx->drw->draw_polygon(drw_data, 1, pts, 3);
}

void
r_line(ImpRenderCtx *ctx, void *drw_data, iks *node)
{
	int x, y, x2, y2;

	fg_color(ctx, drw_data, node, "svg:stroke-color");

	x = r_get_x (ctx, node, "svg:x1");
	y = r_get_y (ctx, node, "svg:y1");
	x2 = r_get_x (ctx, node, "svg:x2");
	y2 = r_get_y (ctx, node, "svg:y2");
	ctx->drw->draw_line(drw_data, x, y, x2, y2);

	if (r_get_style (ctx, node, "draw:marker-start")) {
		r_arrow (ctx, drw_data, node, x2, y2, x, y);
	}
	if (r_get_style (ctx, node, "draw:marker-end")) {
		r_arrow (ctx, drw_data, node, x, y, x2, y2);
	}
}

void
r_rect(ImpRenderCtx *ctx, void *drw_data, iks *node)
{
	char *tmp;
	int x, y, w, h;
	int fill = 1;
	int roundness = 0;

	tmp = r_get_style (ctx, node, "draw:fill");
	if (!tmp || strcmp (tmp, "solid") != 0) fill = 0;

	x = r_get_x (ctx, node, "svg:x");
	y = r_get_y (ctx, node, "svg:y");
	w = r_get_x (ctx, node, "svg:width");
	h = r_get_y (ctx, node, "svg:height");

	tmp = r_get_style (ctx, node, "draw:corner-radius");
	if (tmp) roundness = atof (tmp) * ctx->fact_x;

	if (fill) {
		fg_color(ctx, drw_data, node, "draw:fill-color");
		r_draw_rect (ctx, drw_data, 1, x, y, w, h, roundness);
	}
	fg_color(ctx, drw_data, node, "svg:stroke-color");
	r_draw_rect (ctx, drw_data, 0, x, y, w, h, roundness);

	if (iks_child (node)) {
		//r_text (ctx, node);
	}
}

static int x, y, w, h;
static int px, py, pw, ph;

static void
r_get_viewbox (iks *node)
{
	char *tmp;

	tmp = iks_find_attrib (node, "svg:viewBox");
	if (!tmp) return;
	sscanf (tmp, "%d %d %d %d", &px, &py, &pw, &ph);
}

void
r_polygon(ImpRenderCtx *ctx, void *drw_data, iks *node)
{
	char *data;
	ImpPoint *points;
	int i, cnt, j;
	int num;
	int fill = 1;

	data = r_get_style (ctx, node, "draw:fill");
	if (!data || strcmp (data, "solid") != 0) fill = 0;

	x = r_get_x (ctx, node, "svg:x");
	y = r_get_y (ctx, node, "svg:y");
	w = r_get_x (ctx, node, "svg:width");
	h = r_get_y (ctx, node, "svg:height");
	r_get_viewbox (node);

	data = iks_find_attrib (node, "draw:points");
	points = malloc (sizeof (ImpPoint) * strlen (data) / 4);

	cnt = 0;
	j = 0;
	num = -1;
	for (i = 0; data[i]; i++) {
		if (data[i] >= '0' && data[i] <= '9') {
			if (num == -1) num = i;
		} else {
			if (num != -1) {
				if (j == 0) {
					points[cnt].x = atoi (data + num);
					j = 1;
				} else {
					points[cnt++].y = atoi (data + num);
					j = 0;
				}
				num = -1;
			}
		}
	}
	if (num != -1) {
		if (j == 0) {
			points[cnt].x = atoi (data + num);
		} else {
			points[cnt++].y = atoi (data + num);
		}
	}
	for (i = 0; i < cnt; i++) {
		points[i].x = x + points[i].x * w / pw;
		points[i].y = y + points[i].y * h / ph;
	}

	if (fill) {
		fg_color(ctx, drw_data, node, "draw:fill-color");
		ctx->drw->draw_polygon(drw_data, 1, points, cnt);
	}
	fg_color(ctx, drw_data, node, "svg:stroke-color");
	ctx->drw->draw_polygon(drw_data, 0, points, cnt);

	free (points);
}

void
r_polyline(ImpRenderCtx *ctx, void *drw_data, iks *node)
{
	char *data;
	ImpPoint *points;
	int i, cnt, j;
	int num;
	int pen_x, pen_y;

	x = r_get_x (ctx, node, "svg:x");
	y = r_get_y (ctx, node, "svg:y");
	w = r_get_x (ctx, node, "svg:width");
	h = r_get_y (ctx, node, "svg:height");
	r_get_viewbox (node);

	data = iks_find_attrib (node, "draw:points");
	points = malloc (sizeof (ImpPoint) * strlen (data) / 4);

	cnt = 0;
	j = 0;
	num = -1;
	for (i = 0; data[i]; i++) {
		if (data[i] >= '0' && data[i] <= '9') {
			if (num == -1) num = i;
		} else {
			if (num != -1) {
				if (j == 0) {
					points[cnt].x = atoi (data + num);
					j = 1;
				} else {
					points[cnt++].y = atoi (data + num);
					j = 0;
				}
				num = -1;
			}
		}
	}
	if (num != -1) {
		if (j == 0) {
			points[cnt].x = atoi (data + num);
		} else {
			points[cnt++].y = atoi (data + num);
		}
	}

	pen_x = x + points[0].x * w /pw;
	pen_y = y + points[0].y * h / ph;
	fg_color(ctx, drw_data, node, "svg:stroke-color");
	for (i = 1; i < cnt; i++) {
		int tx, ty;
		tx = x + points[i].x * w / pw;
		ty = y + points[i].y * h / ph;
		ctx->drw->draw_line(drw_data, pen_x, pen_y, tx, ty);
		pen_x = tx;
		pen_y = ty;
	}
	free (points);
}
