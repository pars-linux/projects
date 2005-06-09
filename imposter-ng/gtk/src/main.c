/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"

#ifdef HAVE_GETOPT_LONG
#include <getopt.h>

static struct option longopts[] = {
	{ "help", 0, 0, 'h' },
	{ "version", 0, 0, 'V' },
	{ "slave", 0, 0, 's' },
	{ 0, 0, 0, 0 }
};
#endif

static char *shortopts = "hVs";

static void
print_usage(void)
{
	puts(_("Usage: imposter [OPTIONS] FILE\n"
		"A viewer for your OO.org Impress presentations.\n"
		" -h, --help     Print this text and exit.\n"
		" -V, --version  Print version and exit.\n"
		" -s, --slave    Read commands from stdin."));
#ifndef HAVE_GETOPT_LONG
	printf(_("(long options are not supported on your system)\n"));
#endif
	puts(_("Report bugs to <madcat@e-kolay.net>."));
}


int
main(int argc, char *argv[])
{
	int opt_slave = 0;
	int c;
#ifdef HAVE_GETOPT_LONG
	int i;
#endif

	gtk_set_locale();
	bindtextdomain(PACKAGE, LOCALEDIR);
	bind_textdomain_codeset(PACKAGE, "UTF-8");
	textdomain(PACKAGE);

#ifdef HAVE_GETOPT_LONG
	while ((c = getopt_long(argc, argv, shortopts, longopts, &i)) != -1) {
#else
	while ((c = getopt(argc, argv, shortopts)) != -1) {
#endif
		switch (c) {
			case 's':
				opt_slave = 1;
				break;
			case 'h':
				print_usage();
				exit (0);
			case 'V':
				puts("imposter "VERSION);
				exit (0);
		}
	}

	gtk_init(&argc, &argv);
	ui_setup();
//	info_setup();

	if (opt_slave) slave_start();

	if (optind < argc) {
		if (strcmp(argv[optind], "moo") == 0) {
			/*  8')  */
			puts(_("I don't have any easter eggs... or do I?"));
			exit(0);
		} else {
			ui_open(argv[optind]);
		}
	}

	gtk_main();

	return 0;
}

void
main_quit(void)
{
	gtk_main_quit();
}
