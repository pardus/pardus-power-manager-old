DESTDIR=/

build:
	make -C po build

pot:
	xgettext -o power-manager.pot --from-code="utf-8" src/*.py res/*.ui
	make -C po merge

install:
	mkdir -p $(DESTDIR)/usr/bin || true
	mkdir -p $(DESTDIR)/usr/share/applications/ || true
	mkdir -p $(DESTDIR)/etc/xdg/autostart/ || true
	mkdir -p $(DESTDIR)/usr/share/polkit-1/actions || true
	mkdir -p $(DESTDIR)/usr/lib/pardus/power-manager/tlp || true
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/ || true
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/scalable/actions/ || true
	make -C data install
	make -C po install
	make -C res install
	make -C tlp-conf install
	make -C src install

clean:
	make -C po clean
