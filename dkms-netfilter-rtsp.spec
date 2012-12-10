%define proto rtsp
%define module_name netfilter-%proto

Name:		dkms-%{module_name}
Version:	2.6.26
Release:	%mkrel 2
Epoch:		0
Summary:	Netfilter %proto support (nat and conntrack)
License:	GPLv2
URL:		http://mike.it-loops.com/rtsp/
Source0:	%proto-module-%{version}.tar.gz
Group:		System/Kernel and hardware
Requires(post): coreutils
Requires(post):	dkms
Requires(preun): dkms
Provides:	%{module_name} = %{epoch}:%{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Exclusivearch:	%{ix86} x86_64

%description
This module enable to add conntrack and nat support to netfilter for rtsp,
( Real Time Streaming Protocol ). 

%prep
%setup -q -n %proto

%build

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_usrsrc}/%{module_name}-%{version}-%{release}
%{__cp} -a * %{buildroot}%{_usrsrc}/%{module_name}-%{version}-%{release}
%{__cat} > %{buildroot}%{_usrsrc}/%{module_name}-%{version}-%{release}/dkms.conf << EOF
PACKAGE_VERSION="%{version}-%{release}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{module_name}"

BUILT_MODULE_NAME[0]="nf_conntrack_rtsp"
DEST_MODULE_LOCATION[0]="/kernel/net/netfilter"
BUILT_MODULE_NAME[1]="nf_nat_rtsp"
DEST_MODULE_LOCATION[1]="/kernel/net/netfilter"

AUTOINSTALL="yes"

EOF

%clean
%{__rm} -rf %{buildroot}

%post
%{_sbindir}/dkms add -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade
%{_sbindir}/dkms build -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade
%{_sbindir}/dkms install -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade
/sbin/rmmod nf_conntrack_rtsp
/sbin/modprobe nf_conntrack_rtsp
/sbin/rmmod nf_nat_rtsp
/sbin/modprobe nf_nat_rtsp || :

%preun
%{_sbindir}/dkms remove -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade --all || :

%files
%defattr(0644,root,root,0755)
%doc README
%{_usrsrc}/%{module_name}-%{version}-%{release}



%changelog
* Fri Apr 17 2009 Pascal Terjan <pterjan@mandriva.org> 0:2.6.26-2mdv2009.1
+ Revision: 367931
- Fix post scriplet
- Do not remove /etc/sysconfig/lm_sensors on uninstall
- Fix dkms.conf to list correct module names
- Fix dkms make command

* Tue Jan 20 2009 Michael Scherer <misc@mandriva.org> 0:2.6.26-1mdv2009.1
+ Revision: 331952
- add doc
- import dkms-netfilter-rtsp


