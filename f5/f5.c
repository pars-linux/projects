/*
 * Send fake f5 key event, best suited for refreshing Pardus page
 * while waiting for a release
 *
 * compile with
 * gcc f5.c -lX11 -lXtst -o f5
 *
 * Onur Küçük <onur@pardus.org.tr> 20 Jan 2011
*/


#include <X11/Xlib.h>
#include <X11/Intrinsic.h>
#include <X11/extensions/XTest.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


int repeat = 10;
int sleepinterval = 2;


static void sendPointerMotion(Display * disp, int motionX, int motionY, int relative) {
    XEvent event;

    /* Get the current pointer position */
    XQueryPointer (disp, RootWindow (disp, 0),
                   &event.xbutton.root, &event.xbutton.window,
                   &event.xbutton.x_root, &event.xbutton.y_root,
                   &event.xbutton.x, &event.xbutton.y,
                   &event.xbutton.state);

    if (relative) {
        /* Fake the pointer movement to new relative position */
        XTestFakeMotionEvent(disp, 0, event.xbutton.x + motionX,
                             event.xbutton.y + motionY, 0);

    } else {
        /* Fake the pointer movement to new absolute position */
        XTestFakeMotionEvent (disp, 0, motionX, motionY, 0);
    }

    XSync(disp, False);
}

static void sendPointerClick(Display * disp, int pointerButton) {
    /* Fake the mouse button Press and Release events */
    XTestFakeButtonEvent (disp, pointerButton, True,  0);
    XTestFakeButtonEvent (disp, pointerButton, False, 0);

    XSync(disp, False);
}

/* Send Fake Key Event */
static void sendKey (Display * disp, KeySym keysym, KeySym modsym) {
    KeyCode keycode = 0, modcode = 0;

    keycode = XKeysymToKeycode (disp, keysym);
    if (keycode == 0)
        return;

    XTestGrabControl (disp, True);

    /* Generate modkey press */
    if (modsym != 0) {
        modcode = XKeysymToKeycode(disp, modsym);
        XTestFakeKeyEvent (disp, modcode, True, 0);
    }

    /* Generate regular key press and release */
    XTestFakeKeyEvent (disp, keycode, True, 0);
    XTestFakeKeyEvent (disp, keycode, False, 0);

    /* Generate modkey release */
    if (modsym != 0)
        XTestFakeKeyEvent (disp, modcode, False, 0);

    XSync (disp, False);
    XTestGrabControl (disp, False);
}

void printusage(void) {
    printf("\n");
    printf("Automatic F5 pressing tool, start with \n");
    printf("\n");
    printf("f5 <repeat count> <delay in seconds> \n");
    printf("\n");
    printf("running as repeat=%d delay=%d\n", repeat, sleepinterval);
    printf("\n");
}


int main (int argc, char *argv[]) {

    Display *disp = XOpenDisplay (NULL);
    int i;

    if (argc > 1)
        repeat = atoi(argv[1]);

    if (argc > 2)
        sleepinterval = atoi(argv[2]);

    printusage();

    for (i = 0; i < repeat; i++) {
        sleep (sleepinterval);
        //sendKey (disp, XK_F5, XK_Alt_L);    /* press Alt-F5 */
        //sendPointerClick(disp, 3);          /* click right mouse button */
        //sendPointerMotion(disp, 50, 50, 1); /* move mouse to 50 pixels right and 50 pixel below */

        sendKey (disp, XK_F5, 0);           /* press F5 */

        printf("pressing f5\n");
    }

    XCloseDisplay (disp);
    printf("\n");
    return 0;

}


