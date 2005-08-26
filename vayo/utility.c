#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <sys/stat.h>

#define LOG_FILE ".sonyfn.log"

static char *
get_log_name(void)
{
	static char *name = NULL;
	char *home;

	if (name) return name;

	home = getenv("HOME");
	if (home) {
		name = malloc(strlen(home) + 1 + strlen(LOG_FILE) + 1);
		sprintf(name, "%s/%s", home, LOG_FILE);
	} else {
		name = LOG_FILE;
	}
	return name;
}

void
print_log(const char *fmt, ...)
{
	static char buf[128];
	time_t t;
	struct tm *bt;
	va_list ap;
	FILE *f;

	f = fopen(get_log_name(), "ab");
	if (!f) return;

	time(&t);
	bt = gmtime(&t);
	strftime(buf, 127, "%F %T", bt);
	fputs(buf, f);

	va_start(ap, fmt);
	fputs(" ", f);
	vfprintf(f, fmt, ap);
	fputs("\n", f);
	va_end(ap);

	fclose(f);
}

void
detach_session(void)
{
	pid_t pid, sid;

	pid = fork ();
	if (pid < 0) {
		print_log("fork() failed");
		exit(1);
	}
	// return from parent
	if (pid > 0) exit(0);
	// child continues from now on

	umask(0066);

	sid = setsid();
	if (sid < 0) {
		print_log("setsid() failed");
		exit(1);
	}

	close(STDIN_FILENO);
	close(STDOUT_FILENO);
	close(STDERR_FILENO);
}
