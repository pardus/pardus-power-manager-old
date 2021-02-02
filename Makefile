DESTDIR=/

build:
	true

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
	ln -s ../lib/pardus/power-manager/main.py $(DESTDIR)/usr/bin/pardus-power-manager
	mkdir -p $(DESTDIR)/usr/share/applications/ || true
	install pardus-power-manager.desktop $(DESTDIR)/usr/share/applications/
	mkdir -p $(DESTDIR)/usr/share/polkit-1/actions
	install pardus-power-manager.policy $(DESTDIR)/usr/share/polkit-1/actions
