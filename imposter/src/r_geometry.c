/* imposter (OO.org Impress viewer)
** Copyright (C) 2003 Gurer Ozen <madcat@e-kolay.net>
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "render_ctx.h"
#include <math.h>

int
r_get_color (render_ctx *ctx, iks *node, char *name, GdkColor *col)
{
	char *attr;

	attr = r_get_style (ctx, node, name);
	if (attr && TRUE == gdk_color_parse (attr, col)) return 1;
	return 0;
}

int
r_get_x (render_ctx *ctx, iks *node, char *name)
{
	char *val;

	val = iks_find_attrib (node, name);
	if (!val) return 0;
	return atof (val) * ctx->fact_x;
}

int
r_get_y (render_ctx *ctx, iks *node, char *name)
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
	return atof (tmp) * 64;
}

void
r_circle (render_ctx *ctx, iks *node)
{
	int x, y, w, h, sa, ea;
	gboolean fill = TRUE;
	char *tmp;

	x = r_get_x (ctx, node, "svg:x");
	y = r_get_y (ctx, node, "svg:y");
	w = r_get_x (ctx, node, "svg:width");
	h = r_get_y (ctx, node, "svg:height");
	sa = r_get_angle (node, "draw:start-angle", 0);
	ea = r_get_angle (node, "draw:end-angle", 360 * 64);
	if (ea > sa)
		ea = ea - sa;
	else
		ea = (360 * 64) + ea - sa;

	tmp = r_get_style (ctx, node, "draw:fill");
	if (!tmp || strcmp (tmp, "solid") != 0) fill = FALSE;

	tmp = iks_find_attrib (node, "draw:kind");
	if (iks_strcmp (tmp, "arc") == 0) fill = FALSE;

	gdk_draw_arc (ctx->d, ctx->gc, fill, x, y, w, h, sa, ea);
}

void
r_arrow (render_ctx *ctx, iks *node, int x, int y, int x2, int y2)
{
	GdkPoint pts[4];
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

	gdk_draw_polygon (ctx->d, ctx->gc, TRUE, pts, 3);
}

void
r_line (render_ctx *ctx, iks *node)
{
	int x, y, x2, y2;
	GdkColor col;

	if (r_get_color (ctx, node, "svg:stroke-color", &col)) {
		gdk_gc_set_rgb_fg_color (ctx->gc, &col);
	}

	x = r_get_x (ctx, node, "svg:x1");
	y = r_get_y (ctx, node, "svg:y1");
	x2 = r_get_x (ctx, node, "svg:x2");
	y2 = r_get_y (ctx, node, "svg:y2");
	gdk_draw_line (ctx->d, ctx->gc, x, y, x2, y2);

	if (r_get_style (ctx, node, "draw:marker-start")) {
		r_arrow (ctx, node, x2, y2, x, y);
	}
	if (r_get_style (ctx, node, "draw:marker-end")) {
		r_arrow (ctx, node, x, y, x2, y2);
	}
}

void
r_rect (render_ctx *ctx, iks *node)
{
	char *tmp;
	int x, y, w, h;
	gboolean fill = TRUE;
	int roundness = 0;
	GdkColor col;

	tmp = r_get_style (ctx, node, "draw:fill");
	if (!tmp || strcmp (tmp, "solid") != 0) fill = FALSE;

	x = r_get_x (ctx, node, "svg:x");
	y = r_get_y (ctx, node, "svg:y");
	w = r_get_x (ctx, node, "svg:width");
	h = r_get_y (ctx, node, "svg:height");

	tmp = r_get_style (ctx, node, "draw:corner-radius");
	if (tmp) roundness = atof (tmp) * ctx->fact_x;

	if (fill) {
		if (r_get_color (ctx, node, "draw:fill-color", &col)) {
			gdk_gc_set_rgb_fg_color (ctx->gc, &col);
		}
		r_draw_rect (ctx, TRUE, x, y, w, h, roundness);
	}
	if (r_get_color (ctx, node, "svg:stroke-color", &col)) {
		gdk_gc_set_rgb_fg_color (ctx->gc, &col);
	}
	r_draw_rect (ctx, FALSE, x, y, w, h, roundness);

	if (iks_child (node)) {
		r_text (ctx, node);
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

void r_polygon (render_ctx *ctx, iks *node)
{
	GdkColor col;
	char *data;
	GdkPoint *points;
	int i, cnt, j;
	int num;
	gboolean fill = TRUE;

	data = r_get_style (ctx, node, "draw:fill");
	if (!data || strcmp (data, "solid") != 0) fill = FALSE;

	x = r_get_x (ctx, node, "svg:x");
	y = r_get_y (ctx, node, "svg:y");
	w = r_get_x (ctx, node, "svg:width");
	h = r_get_y (ctx, node, "svg:height");
	r_get_viewbox (node);

	data = iks_find_attrib (node, "draw:points");
	points = malloc (sizeof (GdkPoint) * strlen (data) / 4);

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
		if (r_get_color (ctx, node, "draw:fill-color", &col)) {
			gdk_gc_set_rgb_fg_color (ctx->gc, &col);
		}
		gdk_draw_polygon (ctx->d, ctx->gc, TRUE, points, cnt);
	}
	if (r_get_color (ctx, node, "svg:stroke-color", &col)) {
		gdk_gc_set_rgb_fg_color (ctx->gc, &col);
	}
	gdk_draw_polygon (ctx->d, ctx->gc, FALSE, points, cnt);

	free (points);
}

void r_polyline (render_ctx *ctx, iks *node)
{
	GdkColor col;
	char *data;
	GdkPoint *points;
	int i, cnt, j;
	int num;

	x = r_get_x (ctx, node, "svg:x");
	y = r_get_y (ctx, node, "svg:y");
	w = r_get_x (ctx, node, "svg:width");
	h = r_get_y (ctx, node, "svg:height");
	r_get_viewbox (node);

	data = iks_find_attrib (node, "draw:points");
	points = malloc (sizeof (GdkPoint) * strlen (data) / 4);

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

	r_draw_move (ctx, x + points[0].x * w /pw, y + points[0].y * h / ph);
	if (r_get_color (ctx, node, "svg:stroke-color", &col)) {
		gdk_gc_set_rgb_fg_color (ctx->gc, &col);
	}
	for (i = 1; i < cnt; i++) {
		r_draw_lineto (ctx, x + points[i].x * w / pw, y + points[i].y * h / ph);
	}
	free (points);
}
