Summary:	Utilities for Hollywood plus / DXR3 device driver for Linux
Name:		em8300
Version:	0.18.0
Release:	5
Group:		System/Kernel and hardware
License:	GPL
URL:		http://dxr3.sourceforge.net/
Source0:	http://downloads.sourceforge.net/dxr3/%{name}-nofirmware-%{version}.tar.gz
BuildRequires:	pkgconfig(gtk+-2.0)
# for /usr/share/alsa/alsa.conf
BuildRequires:	alsa-lib
Provides:	perl(em8300)
Requires:	kmod(em8300)

%description
This package contains utilities that can be used by packages
developed for use with the Hollywood plus or DXR3 MPEG
decoder cards.

You'll also need the non-free microcode for the em8300
device to work, you must download that from
http://dxr3.sourceforge.net/download/em8300.bin to
/lib/firmware/.

%package devel
Summary:	Development headers for DXR3 device
Group:		Development/Other
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	libdxr3-devel = %{version}-%{release}

%description devel
This contains the development headers used when building an
application that will make use of the em8300 driver.

%package -n dkms-%{name}
Summary:	Linux kernel module for Hollywood plus / DXR3 devices
Group:	System/Kernel and hardware
Requires(post):	dkms
Requires(preun): dkms
Requires:	em8300

%description -n dkms-%{name}
This package contains the kernel module for the Hollywood plus
or DXR3 MPEG decoder cards.

Install this package if you wish to use such a card and do not
have the driver in your kernel. You should also install
package em8300.

%prep
%setup -q

echo > README.install.urpmi <<EOF
EM8300-devices require a non-free microcode to operate. If you
have not already done so, you have to download
http://dxr3.sourceforge.net/download/em8300.bin to /lib/firmware/.
EOF

if [ -x modules/update_em8300_version.sh ]; then # is snapshot
	# Run by make during module build if it exists, uses hg which users do not have.
	rm modules/update_em8300_version.sh
	echo "#define EM8300_VERSION \"hg-rev-%snapshot\"" > modules/em8300_version.h
fi

%build
%configure2_5x
%make LIBS="-lX11 -lm"

%install
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
install -m644 modules/em8300-udev.rules \
	%{buildroot}%{_sysconfdir}/udev/rules.d/%{name}.rules

install -d -m755 %{buildroot}/usr/src/%{name}-%{version}-%{release}
cp -a modules include %{buildroot}/usr/src/%{name}-%{version}-%{release}
rm -f %{buildroot}/usr/src/%{name}-%{version}-%{release}/modules/em8300-udev.rules
cat > %{buildroot}/usr/src/%{name}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME="%{name}"
PACKAGE_VERSION="%{version}-%{release}"
MAKE[0]="cd modules && make KERNEL_LOCATION=\$kernel_source_dir KERNVER=\$kernelver"
CLEAN="cd modules && make clean"
BUILT_MODULE_NAME[0]="adv717x"
BUILT_MODULE_NAME[1]="bt865"
BUILT_MODULE_NAME[2]="em8300"
BUILT_MODULE_LOCATION[0]="modules"
BUILT_MODULE_LOCATION[1]="modules"
BUILT_MODULE_LOCATION[2]="modules"
DEST_MODULE_LOCATION[0]="/kernel/drivers/video"
DEST_MODULE_LOCATION[1]="/kernel/drivers/video"
DEST_MODULE_LOCATION[2]="/kernel/drivers/video"
AUTOINSTALL=yes
EOF

%post -n dkms-%{name}
dkms add     -m %{name} -v %{version}-%{release} --rpm_safe_upgrade &&
dkms build   -m %{name} -v %{version}-%{release} --rpm_safe_upgrade &&
dkms install -m %{name} -v %{version}-%{release} --rpm_safe_upgrade --force
true

%preun -n dkms-%{name}
dkms remove  -m %{name} -v %{version}-%{release} --rpm_safe_upgrade --all
true

%files
%doc README AUTHORS ChangeLog.old modules/README-* modules/INSTALL README.install.urpmi
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
%{_bindir}/*
%{_datadir}/em8300
%{_datadir}/alsa/cards/EM8300.conf
%{_mandir}/man1/*

%files devel
%{_includedir}/linux/*

%files -n dkms-%{name}
/usr/src/%{name}-%{version}-%{release}


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.18.0-3mdv2011.0
+ Revision: 664132
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.18.0-2mdv2011.0
+ Revision: 605101
- rebuild

* Sat Jan 02 2010 Frederik Himpe <fhimpe@mandriva.org> 0.18.0-1mdv2010.1
+ Revision: 485190
- update to new version 0.18.0

* Thu Oct 01 2009 Anssi Hannula <anssi@mandriva.org> 0.17.4-1mdv2010.0
+ Revision: 452157
- new version

* Wed Jul 15 2009 Anssi Hannula <anssi@mandriva.org> 0.17.3-1mdv2010.0
+ Revision: 396082
- new version

* Fri Mar 20 2009 Anssi Hannula <anssi@mandriva.org> 0.17.2-1mdv2009.1
+ Revision: 359226
- new version

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.17.0-2.hg611.2mdv2009.1
+ Revision: 350925
- rebuild

* Sun Jul 20 2008 Anssi Hannula <anssi@mandriva.org> 0.17.0-2.hg611.1mdv2009.0
+ Revision: 239099
- new snapshot (support for recent kernels, fixes #41826)
- update file list
- require the kernel module

* Sun Apr 27 2008 Anssi Hannula <anssi@mandriva.org> 0.17.0-1mdv2009.0
+ Revision: 197810
- new version

* Fri Feb 08 2008 Anssi Hannula <anssi@mandriva.org> 0.16.4-1mdv2008.1
+ Revision: 164228
- new version

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Nov 30 2007 Anssi Hannula <anssi@mandriva.org> 0.16.3-1.20071130.1mdv2008.1
+ Revision: 114052
- new snapshot (support for recent kernels)

* Wed Sep 05 2007 Anssi Hannula <anssi@mandriva.org> 0.16.3-1mdv2008.0
+ Revision: 80137
- 0.16.3
- require em8300 in dkms-em8300
- do not run next dkms step in %%post if one fails

* Fri May 11 2007 Anssi Hannula <anssi@mandriva.org> 0.16.2-1mdv2008.0
+ Revision: 26322
- 0.16.2
- show microcode notice only on initial installation


* Fri Mar 02 2007 Anssi Hannula <anssi@mandriva.org> 0.16.1-1mdv2007.0
+ Revision: 130900
- fix buildrequires
- 0.16.1
- disallow non-zero exit status of dkms rpm scripts

* Mon Nov 27 2006 Anssi Hannula <anssi@mandriva.org> 0.16.0-2mdv2007.1
+ Revision: 87697
- raise release
- 0.16.0
- Import em8300

* Fri Aug 25 2006 Anssi Hannula <anssi@mandriva.org> 0.15.3-20060824.2mdv2007.0
- drop useless paragraph from description

* Fri Aug 25 2006 Anssi Hannula <anssi@mandriva.org> 0.15.3-20060824.1mdv2007.0
- snapshot (support for recent kernels)
- really include README.urpmi
- fix typo in description

* Tue Jul 11 2006 Anssi Hannula <anssi@mandriva.org> 0.15.3-1mdv2007.0
- 0.15.3
- drop non-free firmware, add notices to description and README.urpmi
- drop HUPing devfsd in %%post, devfsd is obsolete
- use %%buildroot, %%configure2_5x
- buildrequires gtk2-devel instead of gtk-devel now

* Wed Jan 04 2006 Anssi Hannula <anssi@mandriva.org> 0.15.2-1mdk
- 0.15.2
- dkms package
- drop patch1, patch2, fixed upstream
- drop library, unmklibify devel package, obsolete accordingly
- remove em8300setup udev rule, driver now uses hotplug loading
- %%mkrel

* Fri Dec 09 2005 Olivier Blin <oblin@mandriva.com> 0.13.0-10mdk
- add udev rule to run em8300setup
  (migrated dev.d file from the udev package)

