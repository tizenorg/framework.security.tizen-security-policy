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

# ex. redwood8974_eur_open
SEC_BUILD_PROJECT_NAME=%{sec_build_project_name}

# ex. eur_open
OPERATOR=${SEC_BUILD_PROJECT_NAME#*_}

ARCH=%{arch}

%ifarch %{ix86}
ARCH=i586
%else
ARCH=arm
%endif

if [ "$ARCH" = "arm" ]; then
	echo "target"
%if 0%{?tizen_build_binary_release_type_eng}
	echo "release type eng"
	REL_MODE=eng
%else
	REL_MODE=usr
%endif
else
	echo "emulator"
	REL_MODE=emul
fi

#03-04, No more use OPERATOR
%cmake . -DRELMODE=${REL_MODE} # -DOPERATOR=${OPERATOR}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}/usr/share/license
install LICENSE.Apache-2.0 %{buildroot}/usr/share/license/%{name}

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
/usr/share/wrt-engine/*
%attr(664,root,root) /usr/etc/ace/TizenPolicy.xml
%attr(664,root,root) /opt/share/cert-svc/certs/code-signing/tizen/*.pem
%attr(664,root,root) /opt/share/cert-svc/certs/code-signing/wac/*.pem
/usr/share/license/%{name}
