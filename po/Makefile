L=tr
merge:
	for lang in $(L) ; do \
	    msgmerge power-manager-$$lang ../ppm.pot -o $$lang.po ; \
	    rm -f power-manager-$$lang.po ; \
	    mv $$lang.po power-manager-$$lang.po ; \
	done
build:
	for lang in $(L) ; do \
	    msgfmt power-manager-$$lang.po -o power-manager-$$lang.mo ; \
	done
install:
	for lang in $(L) ; do \
	    mkdir -p $(DESTDIR)/usr/share/locale/$$lang/LC_MESSAGES/ || true ; \
	    install power-manager-$$lang.mo $(DESTDIR)/usr/share/locale/$$lang/LC_MESSAGES/pardus-power-manager.mo ; \
	done
clean:
	rm -rf *.mo
