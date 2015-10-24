Name:       tizen-security-policy
Version:    1.2.2.1
Release:    1
License:    Apache-2.0
Summary:    Security policy config file and root CA certificates
Group:      Security Framework/Libraries
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
BuildRequires:    cmake
BuildRequires:    openssl
Requires(post):   coreutils

%description
Security policy config file and root CA certificates

%prep
%setup -q
cp %{SOURCE1001} .

%build

%ifarch %{ix86}
%define ARCH i586
%else
%define ARCH arm
%endif

%if "%{ARCH}" == "arm"
    echo "target"
    echo "release type eng"
%define REL_MODE eng
%else
    echo "emulator"
%define REL_MODE emul
%endif

%cmake . -DRELMODE=%{REL_MODE} -DPROFILE_TARGET=%{?tizen_profile_name}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}/usr/share/license
install LICENSE %{buildroot}/usr/share/license/%{name}

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
/usr/share/wrt-engine/*
%attr(664,root,root) /usr/share/cert-svc/certs/code-signing/tizen/*.pem
%attr(664,root,root) /usr/share/cert-svc/certs/code-signing/wac/*.pem
/usr/share/license/%{name}
