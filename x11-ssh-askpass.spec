# Version of ssh-askpass
%define aversion 1.2.4.1

Summary:	OpenSSH X11 passphrase dialog
Name:		x11-ssh-askpass
Version:	1.2.4
Release:	2
License:	Public Domain
Group:		Networking/Remote access
URL:		http://www.jmknoble.net/software/x11-ssh-askpass/
Source0:	http://www.jmknoble.net/software/x11-ssh-askpass/x11-ssh-askpass-%{aversion}.tar.bz2
Patch0:		x11-ssh-askpass-1.2.4-random.patch
BuildRequires:	imake
BuildRequires:	rman
# http://qa.mandriva.com/show_bug.cgi?id=22736
BuildRequires:	x11-util-cf-files >= 1.0.2
BuildRequires:	gccmakedep
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xt)
Requires:	openssh
Requires: 	openssh-askpass-common
Obsoletes:	ssh-extras, ssh-askpass
Provides:	ssh-extras, ssh-askpass = 5.9p1
Requires(pre):	update-alternatives

%description
This package contains Jim Knoble's X11 passphrase dialog.

%prep

%setup -q -n x11-ssh-askpass-%{aversion}
%patch0 -p1 -b .random

%build
%serverbuild

%configure2_5x \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --libexecdir=%{_libdir}/ssh \
    --with-app-defaults-dir=%{_sysconfdir}/X11/app-defaults


xmkmf -a
make includes

%ifarch x86_64
#perl -pi -e "s|/usr/lib\b|%{_libdir}|g" Makefile
perl -pi -e "s|i586-mandriva-linux-gnu|x86_64-mandriva-linux-gnu|g" Makefile
#perl -pi -e "s|%{_libdir}/gcc/|/usr/lib/gcc/|g" Makefile
perl -pi -e "s|-m32|-m64|g" Makefile
perl -pi -e "s|__i386__|__x86_64__|g" Makefile
%endif

make \
    XAPPLOADDIR=%{_sysconfdir}/X11/app-defaults \
    BINDIR=%{_libdir}/ssh \
    CDEBUGFLAGS="$RPM_OPT_FLAGS" \
    CXXDEBUGFLAGS="$RPM_OPT_FLAGS"

# For some reason the x11-ssh-askpass.1.html file is not created on 10.0/10.1  
# x86_64, so we just do it manually here... (oden)
rm -f x11-ssh-askpass.1x.html x11-ssh-askpass.1x-html
rman -f HTML < x11-ssh-askpass._man > x11-ssh-askpass.1x-html && \
mv -f x11-ssh-askpass.1x-html x11-ssh-askpass.1.html

%install
install -d %{buildroot}%{_libdir}/ssh
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install.man
install -d %{buildroot}%{_libdir}/ssh
install -d %{buildroot}%{_sysconfdir}/X11/app-defaults
install -m0644 SshAskpass.ad %{buildroot}%{_sysconfdir}/X11/app-defaults/SshAskpass
install -m0755 x11-ssh-askpass %{buildroot}%{_libdir}/ssh/
install -m0644 x11-ssh-askpass.man %{buildroot}%{_mandir}/man1/x11-ssh-askpass.1

# cleanup
rm -f %{buildroot}%{_libdir}/ssh/ssh-askpass
rm -f %{buildroot}%{_mandir}/man1/ssh-askpass.1x*

%post
update-alternatives --install %{_libdir}/ssh/ssh-askpass ssh-askpass %{_libdir}/ssh/x11-ssh-askpass 10
update-alternatives --install %{_bindir}/ssh-askpass bssh-askpass %{_libdir}/ssh/x11-ssh-askpass 10

%postun
[ $1 = 0 ] || exit 0
update-alternatives --remove ssh-askpass %{_libdir}/ssh/x11-ssh-askpass
update-alternatives --remove bssh-askpass %{_libdir}/ssh/x11-ssh-askpass

%files
%doc README ChangeLog SshAskpass*.ad x11-ssh-askpass.1.html
%{_libdir}/ssh/x11-ssh-askpass
%{_sysconfdir}/X11/app-defaults/SshAskpass
%{_mandir}/man1/x11-ssh-askpass.1*



%changelog
* Tue Sep 06 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.4-1mdv2012.0
+ Revision: 698453
- import x11-ssh-askpass

