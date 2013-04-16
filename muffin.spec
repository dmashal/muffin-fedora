Name:          muffin
Version:       1.7.3
Release:       1%{?dist}
Summary:       Window and compositing manager based on Clutter

Group:         User Interface/Desktops
License:       GPLv2+
URL:           https://github.com/linuxmint/muffin
# To generate source
# wget https://github.com/linuxmint/muffin/tarball/%%{_internel_version} -O muffin-%%{version}.git%%{_internel_version}.tar.gz
Source0:       http://leigh123linux.fedorapeople.org/pub/muffin/source/muffin-%{version}.tar.gz


BuildRequires: pkgconfig(clutter-1.0) >= 1.7.5
BuildRequires: pkgconfig(pango)
BuildRequires: pkgconfig(libstartup-notification-1.0)
BuildRequires: pkgconfig(gtk+-3.0) >= 3.3.3
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(sm)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: zenity
BuildRequires: gnome-doc-utils
BuildRequires: desktop-file-utils
# Bootstrap requirements
BuildRequires: gtk-doc gnome-common intltool
BuildRequires: pkgconfig(libcanberra)
BuildRequires: pkgconfig(gsettings-desktop-schemas)

Requires: control-center-filesystem
Requires: dbus-x11
Requires: zenity

%description
Muffin is a window and compositing manager that displays and manages
your desktop via OpenGL. Muffin combines a sophisticated display engine
using the Clutter toolkit with solid window-management logic inherited
from the Metacity window manager.

While Muffin can be used stand-alone, it is primarily intended to be
used as the display core of a larger system such as Cinnamon. 
For this reason, Muffin is very extensible via plugins, which
are used both to add fancy visual effects and to rework the window
management behaviors to meet the needs of the environment.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}


%description devel
Header files and libraries for developing Muffin plugins. Also includes
utilities for testing Metacity/Muffin themes.

%prep
%setup -q -n %{name}-%{version}
NOCONFIGURE=1 autoreconf -fi

%build
%configure --disable-static --enable-compile-warnings=minimum

sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

SHOULD_HAVE_DEFINED="HAVE_SM HAVE_XINERAMA HAVE_XFREE_XINERAMA HAVE_SHAPE HAVE_RANDR HAVE_STARTUP_NOTIFICATION"

for I in $SHOULD_HAVE_DEFINED; do
  if ! grep -q "define $I" config.h; then
    echo "$I was not defined in config.h"
    grep "$I" config.h
    exit 1
  else
    echo "$I was defined as it should have been"
    grep "$I" config.h
  fi
done

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

#Remove libtool archives.
rm -rf %{buildroot}/%{_libdir}/*.la

%find_lang %{name}

# Muffin contains a .desktop file so we just need to validate it
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%doc README AUTHORS COPYING NEWS HACKING doc/theme-format.txt
%doc %{_mandir}/man1/muffin.1.*
%doc %{_mandir}/man1/muffin-message.1.*
%{_bindir}/muffin
%{_bindir}/muffin-message
%{_datadir}/applications/*.desktop
%{_datadir}/gnome/wm-properties/muffin-wm.desktop
%{_datadir}/muffin/
%{_libdir}/libmuffin.so.*
%{_libdir}/muffin/
%{_datadir}/GConf/gsettings/muffin-schemas.convert
%{_datadir}/glib-2.0/schemas/org.cinnamon.muffin.gschema.xml
%{_datadir}/gnome-control-center/keybindings/50-muffin-windows.xml

%files devel
%{_bindir}/muffin-theme-viewer
%{_bindir}/muffin-window-demo
%{_includedir}/muffin/
%{_libdir}/libmuffin.so
%{_libdir}/muffin/Meta-3.0.gir
%{_libdir}/pkgconfig/*
%doc %{_mandir}/man1/muffin-theme-viewer.1.*
%doc %{_mandir}/man1/muffin-window-demo.1.*

%changelog
* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 1.1.2-3
- Rebuilt for cogl soname bump

* Fri Jan 25 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.1.2-2
- rebuilt for new cogl .so version

* Wed Oct 24 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.1.2-1
- update to 1.1.2 release
- change build requires style

* Thu Sep 27 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.1.1-1
- update to 1.1.1 release

* Tue Sep 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.1.0-2
- rebuild

* Mon Sep 17 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.1.0-1
- update to 1.1.0 release
- drop cogl patch

* Fri Aug 17 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.6-4
- rebuilt for new cogl version
- patch for new cogl api

* Tue Aug 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.6-3
- update scriptlets
- move gir file to devel

* Tue Aug 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.6-2
- Fix unused-direct-shlib-dependency rpmlint warnings
- remove .gz extension from the man files

* Thu Jul 26 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.6-1
- update to 1.0.6 release

* Wed Jul 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.4-0.1.gitfcea2f1
- update to latest git snapshot
- drop patch
- remove gconf bits

* Mon May 28 2012 leigh scott <leigh123linux@googlemail.com> - 1.0.3-3
- add patch to fix black border issue

* Mon May 28 2012 leigh scott <leigh123linux@googlemail.com> - 1.0.3-2
- rebuilt

* Sat May 05 2012 leigh scott <leigh123linux@googlemail.com> - 1.0.3-1
- update to 1.0.3

* Wed Mar 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.2-2
- rebuilt

* Tue Mar 13 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.2-1
- update to 1.0.2

* Mon Mar 12 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.1-1
- update to 1.0.1 

* Mon Mar 12 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-3
- patch for gtk and cogl changes

* Thu Feb 02 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-2
- make review changes

* Wed Jan 04 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-1
- initial package based on fedora mutter srpm
