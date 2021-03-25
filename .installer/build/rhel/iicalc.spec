Summary: An extensible calculator written in Python.
Name: iicalc
Version: {{pkgver}}
Release: {{pkgrel}}
License: GPLv3
URL: https://turbowafflz.gitlab.io/iicalc.html
Packager: Connor Sample
Requires: bash
Requires: python3

%description
ImaginaryInfinity Calculator is a lightweight, but expandable calculator. It's command line interface is designed to resemble that of some graphing calculators. New functionality can easily be added by downloading plugins with the built in package manager or by placing Python files with additional functions in the plugins directory.

%prep
echo "BUILDROOT = $RPM_BUILD_ROOT"
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/applications
mkdir -p $RPM_BUILD_ROOT/usr/share/icons
mkdir -p $RPM_BUILD_ROOT/usr/share/iicalc
mkdir -p $RPM_BUILD_ROOT/usr/share/iicalc/systemPlugins
mkdir -p $RPM_BUILD_ROOT/usr/share/iicalc/themes
mkdir -p $RPM_BUILD_ROOT/usr/share/iicalc/docs

cp {{maindir}}/.installer/launchers/unix.sh $RPM_BUILD_ROOT/usr/bin/iicalc
cp {{maindir}}/.installer/desktopFiles/iicalc.desktop $RPM_BUILD_ROOT/usr/share/applications/
cp {{maindir}}/iicalc.tiff $RPM_BUILD_ROOT/usr/share/icons/

cp -r {{maindir}}/system/systemPlugins/* $RPM_BUILD_ROOT/usr/share/iicalc/systemPlugins
cp -r {{maindir}}/system/themes/* $RPM_BUILD_ROOT/usr/share/iicalc/themes
cp -r {{maindir}}/templates $RPM_BUILD_ROOT/usr/share/iicalc/
cp -r {{maindir}}/system/docs/* $RPM_BUILD_ROOT/usr/share/iicalc/docs
cp {{maindir}}/README.md $RPM_BUILD_ROOT/usr/share/iicalc/docs/iicalc.md
cp {{maindir}}/main.py $RPM_BUILD_ROOT/usr/share/iicalc/iicalc.py
cp {{maindir}}/requirements.txt $RPM_BUILD_ROOT/usr/share/iicalc/
cp {{maindir}}/messages.txt $RPM_BUILD_ROOT/usr/share/iicalc/
cp {{maindir}}/system/version.txt $RPM_BUILD_ROOT/usr/share/iicalc/
cp {{maindir}}/README.md $RPM_BUILD_ROOT/usr/share/iicalc/
cp {{maindir}}/.installer/configDefaults/rhel.ini $RPM_BUILD_ROOT/usr/share/iicalc/config.ini
exit

%files
%attr(0755, root, root) /usr/bin/*
%attr(0644, root, root) /usr/share/applications/*
%attr(0644, root, root) /usr/share/icons/*
%defattr(0644, root, root 755)
/usr/share/iicalc/*

%post
pip3 install -r /usr/share/iicalc/requirements.txt

%preun
echo -e "\033[38;5;11mWarning: Removing ImaginaryInfinity Calculator does not remove the .iicalc folder in your home directory. If you want to run the portable version of ImaginaryInfinity Calculator again, you will have to delete it.\033[m"

%clean
rm -rf $RPM_BUILD_ROOT/usr/bin
rm -rf $RPM_BUILD_ROOT/usr/share/applications
rm -rf $RPM_BUILD_ROOT/usr/share/icons
rm -rf $RPM_BUILD_ROOT/usr/share/iicalc
