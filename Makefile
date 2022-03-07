DESTDIR=/

build:
	make -C po build

pot:
	xgettext -o ppm.pot --from-code="utf-8" src/*.py ui/*.glade
	make -C po merge

install:
	mkdir -p $(DESTDIR)/usr/bin
	mkdir -p $(DESTDIR)/etc/pardus/
	mkdir -p $(DESTDIR)/usr/share/applications/
	mkdir -p $(DESTDIR)/usr/share/pardus/power-manager
	mkdir -p $(DESTDIR)/usr/share/polkit-1/actions
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/
	chmod +x src/*
	make -C tlp-conf install
	make -C po install
	cp -prfv src ui files/* $(DESTDIR)/usr/share/pardus/power-manager
	install files/ppm.conf $(DESTDIR)/usr/share/pardus/power-manager
	install files/ppm.desktop $(DESTDIR)/usr/share/applications/
	install pardus-power-manager $(DESTDIR)/usr/bin/pardus-power-manager
	install files/ppm.policy $(DESTDIR)/usr/share/polkit-1/actions
	install files/pardus-pm.svg $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/
	ln -s pardus-pm.svg $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/pardus-pm-gnome.svg || true
	ln -s pardus-pm.svg $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/pardus-pm-mode1.svg || true
	ln -s pardus-pm.svg $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/pardus-pm-mode2.svg || true
	ln -s pardus-pm.svg $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/pardus-pm-mode3.svg || true
	ln -s pardus-pm.svg $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/pardus-pm-mode4.svg || true
	ln -s pardus-pm.svg $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/pardus-pm-mode5.svg || true
clean:
	make -C po clean
	find -type f | grep "pyc" | xargs rm -fv || true
	find -type f | grep "glade~" | xargs rm -fv || true
	find -type d | grep "pycache" | xargs rmdir -v || true

