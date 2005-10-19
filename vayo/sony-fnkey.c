#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>

// sound stuff
#include <linux/soundcard.h>

// keys
#define  FN_F2  1       // cut sound
#define  FN_F3  2       // volume -
#define  FN_F4  4       // volume +
#define  FN_F5  8       // Brightness -
#define  FN_F6  16      // Brightness +
#define  FN_F7  32      // LCD/SCREEN
#define  FN_F10 128     // Zoom in
#define  FN_F12 64      // Suspend
#define  S1_BTN 4096    // S1 custom button
#define  S2_BTN 8192    // S2 custom button

// config hard coded :p
#define  MIXER_DEV      "/dev/mixer"

#include "common.h"

// SOUND HANDLER
int get_volume( int *value )
{
	int mixer = open(MIXER_DEV, O_RDONLY);

	if( mixer ) 
	{
		ioctl( mixer, SOUND_MIXER_READ_VOLUME, value );
		close( mixer );
		return 0;
	}
	else
		return 1;
}

int set_volume( int *value )
{
	int mixer = open(MIXER_DEV, O_RDWR);

	if( mixer ) 
	{
		ioctl( mixer, SOUND_MIXER_WRITE_VOLUME, value );
		close( mixer );
		return 0;
	}
	else
		return 1;
}

int volume_up()
{
	int value = 0;

	get_volume( &value );

	if( value < 0x5a5a )
		value += 0x0a0a;
	else
		value = 0x6464;

	set_volume( &value );

	osd_show("Volume", value * 100/ 0x6464);

	return 0;
}

int volume_down()
{
	int value = 0;

	get_volume( &value );

	if( value > 0x0a0a )
		value -= 0x0a0a;
	else
		value = 0;

	set_volume( &value );

	osd_show("Volume", value * 100/ 0x6464);

	return 0;
}

int oldvalue;
int mute()
{
	int value;

	get_volume( &value );

	if( value ) 
	{
		oldvalue = value;
		value=0;
		set_volume( &value );
		osd_show("Volume", 0);
	}
	else 
	{
		if( !oldvalue )
		{
			volume_up();
		}
		else 
		{
			set_volume( &oldvalue );
			osd_show("Volume", oldvalue * 100/ 0x6464);
		}
	}
	
	return 0;
}
// END OF SOUND

/* Return current brightness of the screen */
int getBrightness() 
{
	FILE* handle;
	int ret;

	if(( handle = fopen( "/proc/acpi/sony/brightness", "rb" )) == NULL ) 
	{
		print_log( "Error opening /proc/acpi/sony/brightness" );
		exit( -1 );
	}

	if( fscanf( handle, "%d", &ret) != 1 )
	{
		print_log( "Error reading /proc/acpi/sony/brightness" );
		exit( -1 );
	}

	fclose( handle );
	return ret;
}

/* Set the current brightness of the screen */
void setBrightness( int b ) 
{
	FILE* handle;

	// validate values
	if( b > 8 )
	{
		b = 8;
	}
	else if( b < 1 )
	{
		b = 1;
	}

        if(( handle = fopen( "/proc/acpi/sony/brightness", "wb" )) == NULL )
	{
                print_log( "Error opening /proc/acpi/sony/brightness" );
                exit( -1 );
        }
	
        if( fprintf( handle, "%d", b) !=1 )
	{
                print_log( "Error writing /proc/acpi/sony/brightness" );
                exit( -1 );
        }
        fclose( handle );

	osd_show("Brightness", b * 100.0 / 8.0);
}

void launch_magnifier()
{
    pid_t pid;

    if((pid = fork()) == 0 )
        execl("/usr/kde/3.4/bin/kmag", "kmag", NULL);
}


#define KEY_FILE "/proc/acpi/sony/fnkey"


static void
handle_key(int key)
{
	if (key & FN_F5) {
		setBrightness(getBrightness() - 1);
	}

	if (key & FN_F6) {
		setBrightness(getBrightness() + 1);
	}

	if (key & FN_F2) {
		mute();
	}

	if (key & FN_F3) {
		volume_down();
	}
		
	if (key & FN_F4) {
		volume_up();
	}
    
    if (key & FN_F10) {
		launch_magnifier();
	}
}

static void
listen_keys(void)
{
	FILE *f;
	int key;

	while (1) {
		f = fopen(KEY_FILE, "rb");
		if (!f) {
			print_log("Error opening '"KEY_FILE"': %s'", strerror(errno));
			exit(1);
		}
		if (fscanf(f, "%d", &key) != 1) {
			print_log("Error reading '"KEY_FILE"': %s'", strerror(errno));
			exit(1);
		}
		fclose(f);

		if (key) handle_key(key);
		osd_hide();
		usleep(300000);
	}
}

int
main(void) 
{
	detach_session();
	nice(10);

	osd_init();

	print_log("SonyFN loaded");
	listen_keys();

	return 0;
}
