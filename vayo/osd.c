#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>

#include <xosd.h>

#define XFONTNAME "-bitstream-bitstream vera sans-bold-r-*-*-*-340-*-*-*-*-*-*"

#include "common.h"

static xosd *osd;
static struct timeval start_tv;

void
osd_init(void)
{
	osd = xosd_create(2);
	if (!osd) {
		print_log("xosd_create() failed");
		return;
	}
	xosd_set_pos(osd, XOSD_middle);
	xosd_set_align(osd, XOSD_center);
	xosd_set_font(osd, XFONTNAME);
	xosd_set_colour(osd, "#3450f0");
	xosd_set_outline_offset(osd, 1);
	xosd_set_outline_colour(osd, "#000000");
	//xosd_set_shadow_offset(osd, 1);
	xosd_set_bar_length(osd, 25);
}

void
osd_show(const char *text, int value)
{
	xosd_display(osd, 0, XOSD_string, text);
	xosd_display(osd, 1, XOSD_slider, value);
	xosd_show(osd);
	gettimeofday(&start_tv, NULL);
}

unsigned long
t_elapsed (void)
{
	unsigned long msec;
	struct timeval cur_tv;

	gettimeofday (&cur_tv, NULL);
	msec = (cur_tv.tv_sec * 1000) + (cur_tv.tv_usec / 1000);
	msec -= (start_tv.tv_sec * 1000) + (start_tv.tv_usec / 1000);
	return msec;
}

void
osd_hide(void)
{
	if (t_elapsed() > 1500)
		xosd_hide(osd);
}
