ifneq ($(KERNELRELEASE),)

obj-m := sony_acpi.o

ifeq ($(PATCHLEVEL),4)
include $(TOPDIR)/Rules.make
endif

else

KDIR := /usr/src/linux/
PWD := $(shell pwd)

default:
	$(MAKE) -C $(KDIR) SUBDIRS=$(PWD) modules

endif

clean:
	rm -rf *.[oas] .*.flags *.ko .*.cmd .*.d .*.tmp *.mod.c .tmp_versions
