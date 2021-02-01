DESTDIR=/

install:
	mkdir -p $(DESTDIR)/usr/lib/pardus/power-manager/profiles || true
	install profiles/* $(DESTDIR)/usr/lib/pardus/power-manager/profiles/
	install main.py $(DESTDIR)/usr/lib/pardus/power-manager/
	install main.ui $(DESTDIR)/usr/lib/pardus/power-manager/
	install profile.sh $(DESTDIR)/usr/lib/pardus/power-manager/
	mkdir -p $(DESTDIR)/lib/systemd/system/
	install pardus-power-manager.service $(DESTDIR)/lib/systemd/system/
