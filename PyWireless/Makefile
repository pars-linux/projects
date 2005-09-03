all:
	@echo "PyWireless version 2.0 by S.Çağlar Onur <caglar@uludag.org.tr>"
	@echo
	@echo Install:
	@echo "To install PyWireless simply write \"make install\" as root"
	@echo Uninstall:
	@echo "To uninstall PyWireless simply write \"make uninstall\" as root"

install:
	@echo "PyWireless version 2.0 by S.Çağlar Onur <caglar@uludag.org.tr>"
	@echo
	@install -o root -g root -m0755 PyWireless.py /usr/bin/
	@install -o root -g root -d -m0755 /usr/share/PyWireless
	@install -o root -g root -m0644 images/*.png /usr/share/PyWireless/
	
	@msgfmt po/tr/tr.po -o po/tr/PyWireless.mo
	@install -o root -g root -m0644 po/tr/PyWireless.mo /usr/share/locale/tr/LC_MESSAGES/
	@echo "Installation completed..."
	@echo "To run PyWireless write PyWireless.py"

uninstall:
	@echo "PyWireless version 2.0 by S.Çağlar Onur <caglar@uludag.org.tr>"
	@echo
	@rm -f /usr/bin/PyWireless.py
	@rm -f /usr/share/locale/tr/LC_MESSAGES/PyWireless.mo
	@rm -rf /usr/share/PyWireless
	@echo "PyWireless removed from system..."
