build:
	for lang in tr ; do \
	    msgfmt power-manager-$$lang.po -o power-manager-$$lang.mo ; \
	done
install:
	for lang in tr ; do \
	    mkdir -p $(DESTDIR)/usr/share/locale/$$lang/LC_MESSAGES/ || true ; \
	    install power-manager-$$lang.mo $(DESTDIR)/usr/share/locale/$$lang/LC_MESSAGES/power-manager.mo ; \
	done
clean:
	rm -rf *.mo
