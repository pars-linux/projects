/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"

static void
parse_cmd(gchar *line)
{
	if (strcmp(line, "next") == 0 || strcmp(line, "seek 10") == 0 ) {
		page_next();
	} else if (strcmp(line, "prev") == 0 || strcmp(line, "seek -10") == 0 ) {
		page_prev();
	} else if (strcmp(line, "first") == 0 || strcmp(line, "seek 0 1") == 0 ) {
		page_first();
	} else if (strcmp(line, "last") == 0 || strcmp(line, "seek 100 1") == 0 ) {
		page_last();
	} else if (strcmp(line, "fs") == 0 || strcmp(line, "vo_fullscreen") == 0 ) {
		ui_toggle_fs();
	} else if (strcmp(line, "help") == 0) {
		printf(_("available commands: next, prev, first, last, fs\n"));
	}
}

static gboolean
read_cmd(GIOChannel *gio, GIOCondition cond, gpointer data)
{
	GIOStatus s;
	gchar *line;

	s = g_io_channel_read_line(gio, &line, NULL, NULL, NULL);
	if (G_IO_STATUS_NORMAL == s) {
		strtok(line, "\r\n");
		parse_cmd(line);
		g_free(line);
	}
	return TRUE;
}

void
slave_start(void)
{
	GIOChannel *gio;

	gio = g_io_channel_unix_new(STDIN_FILENO);
	g_io_add_watch(gio, G_IO_IN, read_cmd, NULL);
}
