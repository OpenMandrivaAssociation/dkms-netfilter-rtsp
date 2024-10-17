%define proto rtsp
%define module_name netfilter-%{proto}

Summary:	Netfilter RTSP support (nat and conntrack)
Name:		dkms-%{module_name}
Version:	3.7
Release:	2
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		https://mike.it-loops.com/rtsp/
Source0:	%{proto}-module-%{version}-v2.tar.gz
Source10:	%{name}.rpmlintrc
Requires(post):	coreutils
Requires(post,preun):	dkms
Provides:	%{module_name} = %{EVRD}
BuildArch:	noarch

%description
This module enable to add conntrack and nat support to netfilter for rtsp,
( Real Time Streaming Protocol ).

%files
%defattr(0644,root,root,0755)
%doc README.rst
%{_usrsrc}/%{module_name}-%{version}-%{release}

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

#----------------------------------------------------------------------------

%prep
%setup -q -c

%build

%install
mkdir -p %{buildroot}%{_usrsrc}/%{module_name}-%{version}-%{release}
cp -a * %{buildroot}%{_usrsrc}/%{module_name}-%{version}-%{release}
cat > %{buildroot}%{_usrsrc}/%{module_name}-%{version}-%{release}/dkms.conf << EOF
PACKAGE_VERSION="%{version}-%{release}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{module_name}"

BUILT_MODULE_NAME[0]="nf_conntrack_rtsp"
DEST_MODULE_LOCATION[0]="/kernel/net/netfilter"
BUILT_MODULE_NAME[1]="nf_nat_rtsp"
DEST_MODULE_LOCATION[1]="/kernel/net/netfilter"

AUTOINSTALL="yes"

EOF

