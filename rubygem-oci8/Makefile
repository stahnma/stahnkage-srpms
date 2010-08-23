NAME=rubygem-oci8
SPEC_FILE=SPECS/$(NAME).spec
SOURCE_FILE=ruby-oci8-*.gem
SOURCE_URL=http://rubyforge.org/frs/download.php/65899/ruby-oci8-2.0.4.gem

RPMBUILD := $(shell if test -f /usr/bin/rpmbuild ; then echo /usr/bin/rpmbuild ; else echo "x" ; fi)

RPM_DEFINES =   --define "_specdir $(shell pwd)/SPECS" --define "_rpmdir $(shell pwd)/RPMS" --define "_sourcedir $(shell pwd)/SOURCES" --define  "_srcrpmdir $(shell pwd)/SRPMS" --define "_builddir $(shell pwd)/BUILD"

MAKE_DIRS= $(shell pwd)/SPECS $(shell pwd)/SOURCES $(shell pwd)/BUILD $(shell pwd)/SRPMS $(shell pwd)/RPMS 

.PHONEY: listing listing spec uninstall

rpmcheck:
ifeq ($(RPMBUILD),x)
	$(error "rpmbuild not found, exiting...")
endif
	@mkdir -p $(MAKE_DIRS)

getsource:
	cd SOURCES; wget $(SOURCE_URL)

## use this to build an srpm locally
srpm:  rpmcheck getsource
	@wait 
	$(RPMBUILD) $(RPM_DEFINES)  -bs $(SPEC_FILE)
	@mv -f SRPMS/* .
	@rm -rf BUILD SRPMS RPMS

clean:
	rm -rf BUILD SRPMS RPMS *.rpm SOURCES/$(SOURCE_FILE)
