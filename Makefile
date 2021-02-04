DESTDIR=/

build:
	true

install:
	mkdir -p $(DESTDIR)/usr/lib/pardus/power-manager/ || true
	install main.css $(DESTDIR)/usr/lib/pardus/power-manager/
	install main.py $(DESTDIR)/usr/lib/pardus/power-manager/
	install main.ui $(DESTDIR)/usr/lib/pardus/power-manager/
	install setprofile.py $(DESTDIR)/usr/lib/pardus/power-manager/
	install *.svg $(DESTDIR)/usr/lib/pardus/power-manager/
	mkdir -p $(DESTDIR)/usr/bin || true
	ln -s ../lib/pardus/power-manager/main.py $(DESTDIR)/usr/bin/pardus-power-manager || true
	mkdir -p $(DESTDIR)/usr/share/applications/ || true
	install pardus-power-manager.desktop $(DESTDIR)/usr/share/applications/
	mkdir -p $(DESTDIR)/usr/share/polkit-1/actions
	install pardus-power-manager.policy $(DESTDIR)/usr/share/polkit-1/actions
	mkdir -p $(DESTDIR)/usr/lib/pardus/power-manager/tlp
	cp tlp-conf/* $(DESTDIR)/usr/lib/pardus/power-manager/tlp
