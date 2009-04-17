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

BUILT_MODULE_NAME[0]="\$PACKAGE_NAME"
DEST_MODULE_LOCATION[0]="/kernel/net/netfilter"

AUTOINSTALL="yes"

EOF

%clean
%{__rm} -rf %{buildroot}

%post
%{_sbindir}/dkms add -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade
%{_sbindir}/dkms build -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade
%{_sbindir}/dkms install -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade
/sbin/rmmod %{module_name} > /dev/null 2>&1
/sbin/modprobe %{module_name}

%preun
%{__rm} -f %{_sysconfdir}/sysconfig/lm_sensors
%{_sbindir}/dkms remove -m %{module_name} -v %{version}-%{release} --rpm_safe_upgrade --all || :

%files
%defattr(0644,root,root,0755)
%doc README
%{_usrsrc}/%{module_name}-%{version}-%{release}

