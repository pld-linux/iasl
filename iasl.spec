Summary:	ACPI CA for Linux
Summary(pl.UTF-8):	ACPI CA dla Linuksa
Name:		iasl
Version:	20061109
Release:	1
License:	BSD-like
Group:		Applications/System
#Source0Download: http://www.intel.com/technology/iapc/acpi/license2.htm
Source0:	http://www.intel.com/technology/iapc/acpi/downloads/acpica-unix-%{version}.tar.gz
# Source0-md5:	0ca508dd9bec10fb3b53c72aea6bb6a1
Patch0:		%{name}-make.patch
URL:		http://www.intel.com/technology/iapc/acpi/downloads.htm
BuildRequires:	bison
BuildRequires:	flex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ACPI CA contains iasl, an ASL compiler/decompiler. It compiles ASL
(ACPI Source Language) into AML (ACPI Machine Language). This AML is
suitable for inclusion as a DSDT in system firmware. It also can
disassemble AML, for debugging purposes.

%description -l pl.UTF-8
ACPI CA zawiera iasl - kompilator/dekompilator ASL. Kompiluje ASL
(ACPI Source Language) do AML (ACPI Machine Language). Ten AML nadaje
się do umieszczenia w DSDT firmware'u systemu. iasl potrafi także
disasemblować AML w celach diagnostycznych.

%prep
%setup -q -n acpica-unix-%{version}
%patch0 -p1

# extract license text
sed -e '1,6d;114q' osunixxf.c > LICENSE

%build
%{__make} -C compiler \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -D_LINUX -DACPI_ASL_COMPILER -I../include"

%{__make} -C tools/acpisrc \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -D_LINUX -DACPI_APPLICATION -I../../include"

# doesn't build currently, some code missing (AcpiGbl_Db*)
#%{__make} -C tools/acpiexec \
#	CC="%{__cc}" \
#	CFLAGS="%{rpmcflags} -Wall -D_LINUX -DNDEBUG -D_CONSOLE -DACPI_EXEC_APP -D_MULTI_THREADED -I../../include"

%{__make} -C tools/acpixtract \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -D_LINUX -DACPI_APPLICATION -I../../include"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install compiler/iasl $RPM_BUILD_ROOT%{_bindir}
#install tools/acpiexec/acpiexec $RPM_BUILD_ROOT%{_bindir}
install tools/acpisrc/acpisrc $RPM_BUILD_ROOT%{_bindir}
# XXX: program name collision with pmtools
install tools/acpixtract/acpixtract $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README changes.txt
%attr(755,root,root) %{_bindir}/*
