# G15daemon rpm spec file
#
%define prefix	/usr
Summary: Daemon to control logitech G15 keyboards
Name: g15daemon
Version: 3.0.2
Release: 1
Copyright: GPL
Group: Applications/System
Source: https://gitlab.com/menelkir/g15daemon/-/archive/v1.9.5.4/g15daemon-v1.9.5.4.tar.bz2
URL: http://gitlab.com/menelkir/g15daemon
Distribution: Linux
Vendor: NONE
Packager: Daniel Menelkir <dmenelkir@gmail.com>
Buildroot: /var/tmp/g15daemon-%{PACKAGE_VERSION}-root
Requires: libg15
Provides: g15daemon

%description
G15daemon controls the G15 keyboard, allowing the use of 
all keys through the linux kernel uinput device driver.  
It also controls the use of the keyboard's LCD display, 
allows multiple, simultaneous client applications to connect, 
and gives the user the ability to switch between client 
apps at the press of a button.

%package devel
Summary: G15daemon controls the G15 keyboard and LCD.
Group: System Environment/Libraries
BuildRequires: libg15-devel
Requires: g15daemon
Provides: g15daemon-devel

%description devel
G15daemon controls the G15 keyboard, allowing the use of
all keys through the linux kernel uinput device driver.
It also controls the use of the keyboard's LCD display,
allows multiple, simultaneous client applications to connect,
and gives the user the ability to switch between client
apps at the press of a button.

%prep
%setup

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files 
%defattr(-, root, root)

%doc AUTHORS COPYING LICENSE NEWS README README.usage contrib lang-bindings 
%doc %{_mandir}/man*/*.*
%{prefix}/lib/*.so
%{prefix}/lib/*.so.*
%{prefix}/sbin/*

%files devel
%defattr(-, root, root)

%doc AUTHORS COPYING LICENSE NEWS README README.usage contrib lang-bindings Documentation/README.client_devel
%doc %{_mandir}/man*/*.*

%{prefix}/lib/libg15daemon_client.*
%{prefix}/include/*
