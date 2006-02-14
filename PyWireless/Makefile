all:
	@echo "PyWireless"
	@echo
	@echo Install:
	@echo "To install PyWireless simply write \"make PREFIX=/ install\" as root"
	@echo Uninstall:
	@echo "To uninstall PyWireless simply write \"make PREFIX=/ uninstall\" as root"

install:
	@echo "PyWireless"
	@echo
	@mkdir -p ${PREFIX}/usr/bin/ ${PREFIX}/usr/share/PyWireless ${PREFIX}/usr/share/locale/tr/LC_MESSAGES/
	@install -o root -g root -m0755 PyWireless.py ${PREFIX}/usr/bin/
	@install -o root -g root -d -m0755 ${PREFIX}/usr/share/PyWireless
	@install -o root -g root -m0644 images/*.png ${PREFIX}/usr/share/PyWireless/
	
	@msgfmt po/tr/tr.po -o po/tr/PyWireless.mo
	@install -o root -g root -m0644 po/tr/PyWireless.mo ${PREFIX}/usr/share/locale/tr/LC_MESSAGES/
	@echo "Installation completed..."
	@echo "To run PyWireless write PyWireless.py"

uninstall:
	@echo "PyWireless"
	@echo
	@rm -f ${PREFIX}/usr/bin/PyWireless.py
	@rm -f ${PREFIX}/usr/share/locale/tr/LC_MESSAGES/PyWireless.mo
	@rm -rf ${PREFIX}/usr/share/PyWireless
	@echo "PyWireless removed from system..."
