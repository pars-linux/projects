/* imposter (OO.org Impress viewer)
** Copyright (C) 2003-2005 Gurer Ozen
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include "common.h"
#include "render.h"

/* Ignore some modifier keys in keyboard handling. */
#define imposter_ignore_modifiers(a) ((a) &(~(GDK_LOCK_MASK|GDK_MOD2_MASK)))

static GtkWidget *menu_bar, *window, *area;
static ImpDoc *doc;
static char *doc_name;
static int full_screen;

static void ui_perth(void);
static void page_step(void);

static struct {
	char *key;
	void (*func)(void);
} defkeys [] = {
	{ "space", page_step },
	{ "Page_Down", page_next },
	{ "Right", page_next },
	{ "Page_Up", page_prev },
	{ "Left", page_prev },
	{ "Home", page_first },
	{ "End", page_last },
	{ "f", ui_toggle_fs },
	{ "g", ui_perth },
	{ "d", debug_show },
	{ "Escape", main_quit },
	{ NULL, NULL }
};

static const GtkTargetEntry dnd_types[] = {
	{ "text/plain", 0, 0 },
	{ "text/uri-list", 0, 0 },
	{ "STRING", 0, 0 },
};

static gint
cb_key(GtkWidget *win, GdkEventKey *ev, gpointer data)
{
	char *key;
	int i;

	if (imposter_ignore_modifiers(ev->state)) return FALSE;

	key = gdk_keyval_name(ev->keyval);
	if (key) {
		for (i = 0; defkeys[i].key; i++) {
			if (strcmp(key, defkeys[i].key) == 0) {
				defkeys[i].func();
				return TRUE;
			}
		}
	}
	return FALSE;
}

void
ui_open(const char *filename)
{
	ImpDoc *tdoc;
	GtkWidget *d;
	int e;

	tdoc = imp_open(filename, &e);
	if (!tdoc) {
		d = gtk_message_dialog_new (GTK_WINDOW(window),
			GTK_DIALOG_DESTROY_WITH_PARENT,
			GTK_MESSAGE_ERROR, GTK_BUTTONS_CLOSE,
			_("Cannot open file:\n\n'%s'\nError %d."), filename, e);
		g_signal_connect_swapped(G_OBJECT(d), "response", G_CALLBACK(gtk_widget_destroy), G_OBJECT(d));
		gtk_window_present(GTK_WINDOW(d));
		return;
	}
	if (doc) imp_close(doc);
	if (doc_name) free(doc_name);
	doc = tdoc;
	doc_name = strdup(filename);
	debug_update(doc);
	page_first();
}

static void
cb_open(void)
{
	static GtkWidget *sfw = NULL;

	if (!sfw) sfw = sf_new(FALSE, window, _("Select a presentation file..."), (sf_func *)ui_open);
	sf_ask(sfw, NULL);
}

static void
cb_dnd_receive(GtkWidget *w, GdkDragContext *con, gint x, gint y, GtkSelectionData *sdata, guint info, guint time, gpointer udata)
{
	char *t;

	if (sdata->data) {
		t = (char *) sdata->data;
		strtok(t, "\r");
		if (strncmp(t, "file:///", 8) == 0) t += 7;
		if (strncmp(t, "file:/", 6) == 0) t += 5;
		ui_open(t);
	}
}

static gboolean
cb_win_state(GtkWidget *w, GdkEventWindowState *ev, gpointer data)
{
	if (ev->new_window_state & GDK_WINDOW_STATE_FULLSCREEN) {
		full_screen = 1;
		oo_render_step_mode(OO_RENDER(area), 1);
	} else {
		full_screen = 0;
		oo_render_step_mode(OO_RENDER(area), 0);
	}
	return FALSE;
}

void
ui_toggle_fs(void)
{
	if (full_screen) {
		gtk_widget_show(menu_bar);
		gtk_window_unfullscreen(GTK_WINDOW(window));
	} else {
		gtk_widget_hide(menu_bar);
		gtk_window_fullscreen(GTK_WINDOW(window));
	}
}

static void
cb_page_changed(GtkWidget *w, ImpPage *page, gpointer data)
{
	char *title, *file;

	file = g_path_get_basename(doc_name);
	title = g_strdup_printf("%s - %d - %s",
		file,
		imp_get_page_no(page),
		imp_get_page_name(page)
	);
	gtk_window_set_title(GTK_WINDOW(window), title);
	g_free(title);
	g_free(file);
}

static void
ui_clean(void)
{
	gtk_window_set_title(GTK_WINDOW(window), "Imposter");
}

void
ui_setup(void)
{
	GtkItemFactoryEntry menus[] = {
		{ _("/_File"), NULL, NULL, 0, "<Branch>" },
		{ _("/File/_Open..."), NULL, cb_open, 0, "<StockItem>", GTK_STOCK_OPEN },
		{ _("/File/separator"), NULL, NULL, 0, "<Separator>" },
//		{ _("/File/Proper_ties"), NULL, info_show, 0, "<StockItem>", GTK_STOCK_PROPERTIES },
		{ _("/File/separator"), NULL, NULL, 0, "<Separator>" },
//		{ _("/File/_Close"), NULL, doc_close, 0, "<StockItem>", GTK_STOCK_CLOSE },
		{ _("/File/_Quit"), NULL, main_quit, 0, "<StockItem>", GTK_STOCK_QUIT },
		{ _("/_View"), NULL, NULL, 0, "<Branch>" },
		{ _("/View/_Fullscreen"), NULL, ui_toggle_fs, 0, NULL },
		{ _("/_Go"), NULL, NULL, 0, "<Branch>" },
		{ _("/Go/_Previous Page"), NULL, page_prev, 0, "<StockItem>", GTK_STOCK_GO_BACK },
		{ _("/Go/_Next Page"), NULL, page_next, 0, "<StockItem>", GTK_STOCK_GO_FORWARD },
		{ _("/Go/separator"), NULL, NULL, 0, "<Separator>" },
		{ _("/Go/_First Page"), NULL, page_first, 0, "<StockItem>", GTK_STOCK_GOTO_FIRST },
		{ _("/Go/_Last Page"), NULL, page_last, 0, "<StockItem>", GTK_STOCK_GOTO_LAST },
		{ _("/_Help"), NULL, NULL, 0, "<Branch>" },
		{ _("/Help/_About"), NULL, about_show, 0, NULL }
	};
	GtkItemFactory *fabrika;
	GtkAccelGroup *agrp;
	gint n = sizeof(menus) / sizeof(menus[0]);
	GtkWidget *win, *vb, *bar;

	win = gtk_window_new(GTK_WINDOW_TOPLEVEL);
	window  = win;
	gtk_window_set_default_size(GTK_WINDOW(win), 500, 380);
	g_signal_connect(G_OBJECT(win), "delete_event", G_CALLBACK(main_quit), NULL);
	g_signal_connect(G_OBJECT(win), "key_press_event", G_CALLBACK(cb_key), NULL);
	g_signal_connect(G_OBJECT(win), "window_state_event", G_CALLBACK(cb_win_state), NULL);

	vb = gtk_vbox_new(FALSE, 0);
	gtk_widget_show(vb);
	gtk_container_add(GTK_CONTAINER(win), vb);

	agrp = gtk_accel_group_new();
	fabrika = gtk_item_factory_new(GTK_TYPE_MENU_BAR, "<main>", agrp);
	gtk_item_factory_create_items(fabrika, n, menus, NULL);
	gtk_window_add_accel_group(GTK_WINDOW(win), agrp);

	bar = gtk_item_factory_get_widget(fabrika, "<main>");
	menu_bar = bar;
	gtk_widget_show(bar);
	gtk_box_pack_start(GTK_BOX(vb), bar, FALSE, FALSE, 0);

	area = oo_render_new();
	gtk_widget_show(area);
	g_signal_connect(G_OBJECT(area), "page_changed", G_CALLBACK(cb_page_changed), NULL);
	gtk_box_pack_start(GTK_BOX(vb), area, TRUE, TRUE, 0);

	gtk_drag_dest_set(GTK_WIDGET(area), GTK_DEST_DEFAULT_ALL, dnd_types, 3, GDK_ACTION_COPY | GDK_ACTION_MOVE);
	g_signal_connect(G_OBJECT(area), "drag-data-received", G_CALLBACK(cb_dnd_receive), NULL);

	ui_clean();

	gtk_widget_show(win);
}

/*  >:)  */
static void
win_perth(GtkWindow *w, int a, int b)
{
	int x, y;

	gtk_window_get_position(w, &x, &y);
	gtk_window_move(w, x + a, y + b);
}

/*  >:)  */
static void
ui_perth(void)
{
	int i, j;

	if (full_screen) return;
	for (i = 6; i >0; i--) {
		for (j = 5; j > 0; j--) {
			win_perth(GTK_WINDOW(window), 0, i);
			win_perth(GTK_WINDOW(window), i, 0);
			win_perth(GTK_WINDOW(window), 0, -i);
			win_perth(GTK_WINDOW(window), -i, 0);
		}
	}
}

static void
page_step(void)
{
	oo_render_step(OO_RENDER(area));
}

void
page_first(void)
{
	if (doc) {
		oo_render_set_page(OO_RENDER(area), imp_get_page(doc, 0));
	}
}

void
page_next(void)
{
	if (doc) {
		ImpPage *page;
		page = oo_render_get_page(OO_RENDER(area));
		page = imp_next_page(page);
		if (page) oo_render_set_page(OO_RENDER(area), page);
	}
}

void
page_prev(void)
{
	if (doc) {
		ImpPage *page;
		page = oo_render_get_page(OO_RENDER(area));
		page = imp_prev_page(page);
		if (page) oo_render_set_page(OO_RENDER(area), page);
	}
}

void
page_last(void)
{
	if (doc) {
		oo_render_set_page(OO_RENDER(area), imp_get_page(doc, IMP_LAST_PAGE));
	}
}
