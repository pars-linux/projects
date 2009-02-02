#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TARGET "/sys/devices/platform/applesmc.768/leds/smc::kbd_backlight/brightness"

int limited(int inp) {
    if (inp<0) return 0;
    if (inp>255) return 255;
    return inp;
}

int main(int argc, char *argv[]) {
    int current=0,new=0;
    char tempC[10];
    FILE *fp = fopen(TARGET,"r");
    fread(tempC,4,1,fp);
    fclose(fp);
    fp = fopen(TARGET,"w");
    current=atoi(tempC);
    printf("Current : %d\n",current);
    if (argc>=2) {
        if (!strcmp(argv[1],"plus"))
            new = limited(current + 10);
        if (!strcmp(argv[1],"minus"))
            new = limited(current - 10);
        if (!strcmp(argv[1],"set") && argc==3)
            new = limited((int)argv[3]);
        printf("New : %d\n",new);
        fprintf(fp,"%d",new);
    }
    else printf("Usage : %s plus or minus\n",argv[0]);
    fclose(fp);
    return 0;
}
