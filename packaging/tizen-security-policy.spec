Name:		tizen-security-policy
Version:	1.2.2.1
Release:	1
License:	Apache-2.0
Summary:	Security policy config file and root CA certificates
Group:		Security Framework/Libraries
Source0:	%{name}-%{version}.tar.gz
Source1001:	%{name}.manifest

BuildRequires:	cmake
BuildRequires:	openssl
#BuildRequires:	build-info

# runtime requires
Requires(post):		/sbin/ldconfig
Requires(post):		coreutils
Requires(postun):	/sbin/ldconfig

%description
Security policy config file and root CA certificates

%prep
%setup -q
cp %{SOURCE1001} .

%build

ARCH=%{arch}

# default variables
REL_MODE=eng
PROFILE_TARGET=mobile

%ifarch %{ix86}
ARCH=i586
%else
ARCH=arm
%endif

if [ "$ARCH" = "arm" ]; then
	echo "arch arm : eng"
	REL_MODE=eng
else
	echo "arch not arm : emul"
	REL_MODE=emul
fi

%if "%{?tizen_profile_name}" == "mobile"
    PROFILE_TARGET=mobile
%endif
%if "%{?tizen_profile_name}" == "wearable"
    PROFILE_TARGET=wearable
%endif

%cmake . -DRELMODE=${REL_MODE} -DPROFILE_TARGET=${PROFILE_TARGET}

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
%attr(664,root,root) /usr/etc/ace/TizenPolicy.xml
%attr(664,root,root) /usr/share/cert-svc/certs/code-signing/tizen/*.pem
%attr(664,root,root) /usr/share/cert-svc/certs/code-signing/wac/*.pem
/usr/share/license/%{name}
