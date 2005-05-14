/* imposter (OO.org Impress viewer)
** Copyright (C) 2003 Gurer Ozen <madcat@e-kolay.net>
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "render_ctx.h"

typedef struct path_ctx_s {
	int x, y, w, h;	/* box in the page */
	int sx, sy, sw, sh;	/* svg box */
	float fx, fy;	/* scale factors */
	int px, py;	/* pen */
	int cx, cy;	/* control point of last curve */
} path_ctx;

static void
r_get_viewbox (render_ctx *ctx, path_ctx *pc, iks *node)
{
	char *tmp;

	pc->x = r_get_x (ctx, node, "svg:x");
	pc->y = r_get_y (ctx, node, "svg:y");
	pc->w = r_get_x (ctx, node, "svg:width");
	pc->h = r_get_y (ctx, node, "svg:height");
	tmp = iks_find_attrib (node, "svg:viewBox");
	if (!tmp) return;
	sscanf (tmp, "%d %d %d %d", &pc->sx, &pc->sy, &pc->sw, &pc->sh);
	pc->fx = (float) pc->w / pc->sw;
	pc->fy = (float) pc->h / pc->sh;
}

static void
move_to (render_ctx *ctx, path_ctx *pc, iks *node, int *args)
{
	pc->px = args[0] * pc->fx;
	pc->py = args[1] * pc->fy;
}

static void
move_to_rel (render_ctx *ctx, path_ctx *pc, iks *node, int *args)
{
	pc->px += args[0] * pc->fx;
	pc->py += args[1] * pc->fy;
}

static void
line_to (render_ctx *ctx, path_ctx *pc, iks *node, int *args)
{
	int gx, gy;

	gx = args[0] * pc->fx;
	gy = args[1] * pc->fy;
	gdk_draw_line (ctx->d, ctx->gc, pc->x + pc->px, pc->y + pc->py, pc->x + gx, pc->y + gy);
	pc->px = gx;
	pc->py = gy;
}

static void
line_to_rel (render_ctx *ctx, path_ctx *pc, iks *node, int *args)
{
	int gx, gy;

	gx = pc->px + args[0] * pc->fx;
	gy = pc->py + args[1] * pc->fy;
	gdk_draw_line (ctx->d, ctx->gc, pc->x + pc->px, pc->y + pc->py, pc->x + gx, pc->y + gy);
	pc->px = gx;
	pc->py = gy;
}

static void
hline_to (render_ctx *ctx, path_ctx *pc, iks *node, int *args)
{
	int gx;

	gx = args[0] * pc->fx;
	gdk_draw_line (ctx->d, ctx->gc, pc->x + pc->px, pc->y + pc->py, pc->x + gx, pc->py);
	pc->px = gx;
}

static void
hline_to_rel (render_ctx *ctx, path_ctx *pc, iks *node, int *args)
{
	int gx;

	gx = pc->px + args[0] * pc->fx;
	gdk_draw_line (ctx->d, ctx->gc, pc->x + pc->px, pc->y + pc->py, pc->x + gx, pc->py);
	pc->px = gx;
}

static void
vline_to (render_ctx *ctx, path_ctx *pc, iks *node, int *args)
{
	int gy;

	gy = args[0] * pc->fy;
	gdk_draw_line (ctx->d, ctx->gc, pc->x + pc->px, pc->y + pc->py, pc->x + pc->px, pc->y + gy);
	pc->py = gy;
}

static void
vline_to_rel (render_ctx *ctx, path_ctx *pc, iks *node, int *args)
{
	int gy;

	gy = pc->py + args[0] * pc->fy;
	gdk_draw_line (ctx->d, ctx->gc, pc->x + pc->px, pc->y + pc->py, pc->x + pc->px, pc->y + gy);
	pc->py = gy;
}

static void
curve_to_rel (render_ctx *ctx, path_ctx *pc, iks *node, int *args)
{
	int gx, gy;
	int cx1, cy1, cx2, cy2;

	gx = pc->px + (args[4] * pc->fx);
	gy = pc->py + (args[5] * pc->fy);
	cx1 = pc->px + (args[0] * pc->fx);
	cy1 = pc->py + (args[1] * pc->fy);
	cx2 = pc->px + (args[2] * pc->fx);
	cy2 = pc->py + (args[3] * pc->fy);
	pc->cx = cx2;
	pc->cy = cy2;
	draw_bezier (ctx->d, ctx->gc, pc->x + pc->px, pc->y + pc->py, pc->x + cx1, pc->y + cy1, pc->x + cx2, pc->y + cy2, pc->x + gx, pc->y + gy);
	pc->px = gx;
	pc->py = gy;
}

static void
scurve_to_rel (render_ctx *ctx, path_ctx *pc, iks *node, int *args)
{
	int gx, gy;
	int cx1, cy1, cx2, cy2;

	gx = pc->px + (args[2] * pc->fx);
	gy = pc->py + (args[3] * pc->fy);
	cx2 = pc->px + (args[0] * pc->fx);
	cy2 = pc->py + (args[1] * pc->fy);
	cx1 = pc->px + (pc->px - pc->cx);
	cy1 = pc->py + (pc->py - pc->cy);
	pc->cx = cx2;
	pc->cy = cy2;
	draw_bezier (ctx->d, ctx->gc, pc->x + pc->px, pc->y + pc->py, pc->x + cx1, pc->y + cy1, pc->x + cx2, pc->y + cy2, pc->x + gx, pc->y + gy);
	pc->px = gx;
	pc->py = gy;
}

static void
error_to (render_ctx *ctx, path_ctx *pc, iks *node, int *args)
{
	puts ("booo!\n");
}

static struct {
	void (*func)(render_ctx *ctx, path_ctx *pc, iks *node, int *args);
	int nr_arg;
	char cmd;
	char next_cmd;
} cmds[] = {
	{ error_to, 2, 'e', 'e' },
	{ move_to, 2, 'M', 'L' },
	{ move_to_rel, 2, 'm', 'l' },
	{ line_to, 2, 'L', 'L' },
	{ line_to_rel, 2, 'l', 'l' },
	{ hline_to, 1, 'H', 'H' },
	{ hline_to_rel, 1, 'h', 'h' },
	{ vline_to, 1, 'V', 'V' },
	{ vline_to_rel, 1, 'v', 'v' },
	{ curve_to_rel, 6, 'c', 'c' },
	{ scurve_to_rel, 4, 's', 's' },
	{ NULL, 0, 0, 0 }
};

static int
find_cmd (char c)
{
	int i;

	for (i = 0; cmds[i].func; i++) {
		if (cmds[i].cmd == c) return i;
	}
	return 0;
}

void
r_path (render_ctx *ctx, iks *node)
{
	path_ctx pc;
	char *data;
	int args[6];
	int i, cur_arg, num, neg, cmd;

	memset (&pc, 0, sizeof (pc));
	r_get_viewbox (ctx, &pc, node);

	data = iks_find_attrib (node, "svg:d");
	cur_arg = 0;
	num = -1;
	neg = 0;
	cmd = 0;
	for (i = 0; data[i]; i++) {
		if (data[i] >= '0' && data[i] <= '9') {
			if (num == -1) num = i;
		} else {
			if (num != -1) {
				args[cur_arg] = atoi (data + num);
				if (neg) {
					args[cur_arg] = - args[cur_arg];
					neg = 0;
				}
				cur_arg++;
				num = -1;
				if (cur_arg == cmds[cmd].nr_arg) {
					cmds[cmd].func (ctx, &pc, node, &args[0]);
					cmd = find_cmd (cmds[cmd].next_cmd);
					cur_arg = 0;
				}
			}
		}
		if (data[i] == '-') neg = 1;
		if (find_cmd (data[i]) != 0) cmd = find_cmd (data[i]);
	}
	if (num != -1) {
		args[cur_arg] = atoi (data + num);
		if (neg) args[cur_arg] = - args[cur_arg];
		cur_arg++;
		if (cur_arg == cmds[cmd].nr_arg) {
			cmds[cmd].func (ctx, &pc, node, &args[0]);
		}
	}
}
