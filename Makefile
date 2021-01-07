GITVER := $(shell git describe HEAD | tr '-' '+')
APPNAME := yaia

all:
	rm -rf dist/opt
	mkdir -p dist/opt/$(APPNAME)
	npm install bower
	node_modules/bower/bin/bower install
	cp -r app dist/opt/$(APPNAME)
	cp -r migrations dist/opt/$(APPNAME)
	cp -r manage.py dist/opt/$(APPNAME)
	cp requirements.txt dist/opt/$(APPNAME)
	mkdir -p dist/etc/uwsgi/apps-available
	cp $(APPNAME).ini dist/etc/uwsgi/apps-available
	cp dist/DEBIAN/control.templ dist/DEBIAN/control
	mkdir -p dist/var/log/$(APPNAME)
	sed -i 's/%VERSION%/$(GITVER)-1/' dist/DEBIAN/control
	bin/git2debchangelog.sh > dist/DEBIAN/changelog
	dpkg-deb --root-owner-group --nocheck --build dist $(APPNAME)_$(GITVER)-1_all.deb
	echo "$(APPNAME)_$(GITVER)-1_all.deb custom optional" > dist/DEBIAN/files
	dpkg-genchanges -b -ldist/DEBIAN/changelog -cdist/DEBIAN/control -fdist/DEBIAN/files -u. -O$(APPNAME)_$(GITVER)-1_all.changes
