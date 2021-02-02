DESTDIR=/

install:
	mkdir -p $(DESTDIR)/usr/lib/pardus/power-manager/profiles || true
	install profiles/* $(DESTDIR)/usr/lib/pardus/power-manager/profiles/
	install main.py $(DESTDIR)/usr/lib/pardus/power-manager/
	install main.ui $(DESTDIR)/usr/lib/pardus/power-manager/
	install *.svg $(DESTDIR)/usr/lib/pardus/power-manager/
	install profile.sh $(DESTDIR)/usr/lib/pardus/power-manager/
	mkdir -p $(DESTDIR)/lib/systemd/system/ || true
	install pardus-power-manager.service $(DESTDIR)/lib/systemd/system/
	mkdir -p $(DESTDIR)/usr/bin || true
	install pardus-power-manager $(DESTDIR)/usr/bin
	mkdir -p $(DESTDIR)/usr/share/applications/ || true
	install pardus-power-manager.desktop $(DESTDIR)/usr/share/applications/
