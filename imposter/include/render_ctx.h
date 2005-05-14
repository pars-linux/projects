/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen <madcat@e-kolay.net>
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

typedef struct render_ctx_s {
	GdkDrawable *d;
	GdkGC *gc;
	PangoContext *pango_ctx;
	/* content */
	OODoc *doc;
	iks *content, *styles;
	/* page */
	int page_no;
	int step, step_cnt, step_mode;
	/* area */
	float cm_w, cm_h;
	int pix_w, pix_h;
	float fact_x, fact_y;
	int start_x, start_y;
	/* temp */
	int pen_x, pen_y;
} render_ctx;

char *r_get_style (render_ctx *ctx, iks *node, char *attr);
iks *r_get_bullet (render_ctx *ctx, iks *node, char *attr);
void r_group (render_ctx *ctx, iks *node);
void r_page (render_ctx *ctx, iks *page);

void r_draw_pixbuf (render_ctx *ctx, char *name, int x, int y, int w, int h);
void r_tile_pixbuf (render_ctx *ctx, char *name, int x, int y, int w, int h);
void r_draw_move (render_ctx *ctx, int x, int y);
void r_draw_lineto (render_ctx *ctx, int x, int y);
void r_draw_curveto (render_ctx *ctx, int x, int y, int c1x, int c1y, int c2x, int c2y);
void r_draw_rect (render_ctx *ctx, gboolean fill, int x, int y, int w, int h, int roundness);

void r_draw_gradient (render_ctx *ctx, iks *node);

void r_image (render_ctx *ctx, iks *node);

int r_get_color (render_ctx *ctx, iks *node, char *name, GdkColor *col);
int r_get_x (render_ctx *ctx, iks *node, char *name);
int r_get_y (render_ctx *ctx, iks *node, char *name);
void r_circle (render_ctx *ctx, iks *node);
void r_line (render_ctx *ctx, iks *node);
void r_rect (render_ctx *ctx, iks *node);
void r_polygon (render_ctx *ctx, iks *node);
void r_polyline (render_ctx *ctx, iks *node);

void r_text (render_ctx *ctx, iks *node);

void r_path (render_ctx *ctx, iks *node);
