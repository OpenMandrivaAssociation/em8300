%global optflags %{optflags} -fcommon

Summary:	Utilities for Hollywood plus / DXR3 device driver for Linux
Name:		em8300
Version:	0.18.0
Release:	15
Group:		System/Kernel and hardware
License:	GPLv2
Url:		https://dxr3.sourceforge.net/
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
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libdxr3-devel = %{version}-%{release}

%description devel
This contains the development headers used when building an
application that will make use of the em8300 driver.

%package -n dkms-%{name}
Summary:	Linux kernel module for Hollywood plus / DXR3 devices
Group:	System/Kernel and hardware
Requires(post,preun):	dkms
Requires:	em8300

%description -n dkms-%{name}
This package contains the kernel module for the Hollywood plus
or DXR3 MPEG decoder cards.

Install this package if you wish to use such a card and do not
have the driver in your kernel. You should also install
package em8300.

%prep
%autosetup -p1

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
%configure
%make_build  LIBS="-lX11 -lm"

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

