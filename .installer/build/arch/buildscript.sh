#!/usr/bin/env bash
if printf '%s\n' "$@" | grep -q -P '^--beta$|^-b$'; then
  beta=true
else
  beta=false
fi

rm -rf "iicalc-arch"
mkdir -p "iicalc-arch"
cp .installer/build/arch/iicalc.install .installer/build/arch/PKGBUILD "iicalc-arch/"

# Build deb if not exists
if [ ! -f iicalc.deb ]; then
  bash installer.sh --make-deb
fi

if [ "$beta" == "true" ]; then
  sed -i 's/{{pkgname}}/iicalc-beta/g' iicalc-arch/PKGBUILD
else
  sed -i 's/{{pkgname}}/iicalc/g' iicalc-arch/PKGBUILD
fi

# Split version into ver and verrel
version=$(cat system/version.txt)
versionarr=(${version//-/ })
if [ "${#versionarr[@]}" -eq "1" ]; then
  versionarr+=('1')
fi

sed -i "s/{{pkgver}}/${versionarr[0]}/g" iicalc-arch/PKGBUILD
sed -i "s/{{pkgrel}}/${versionarr[1]}/g" iicalc-arch/PKGBUILD

# pkgdesc
if [ "$beta" == "true" ]; then
  desc="\"An extensible calculator written in Python. Development\/Beta Channel.\""
else
  desc="\"An extensible calculator written in Python.\""
fi
sed -i "s/{{pkgdesc}}/$desc/g" iicalc-arch/PKGBUILD

# conflicts
if [ "$beta" == "true" ]; then
  sed -i 's/{{conflicts}}/(\"iicalc\")/g' iicalc-arch/PKGBUILD
else
  sed -i 's/{{conflicts}}/(\"iicalc-beta\")/g' iicalc-arch/PKGBUILD
fi

#sha256 of deb
sed -i "s/{{sha512sums}}/(\'$(sha512sum iicalc.deb | awk '{print $1}')\')/g" iicalc-arch/PKGBUILD

# Update .install file
sed -i '/{{postinst}}/{
  s/{{postinst}}//g
  r .installer/build/deb/postinst
}' iicalc-arch/iicalc.install
sed -i '/{{prerm}}/{
  s/{{prerm}}//g
  r .installer/build/deb/prerm
}' iicalc-arch/iicalc.install

# Clean .install file
sed -i 's/#!\/bin\/sh//g' iicalc-arch/iicalc.install
sed -i ':a;N;$!ba;s/\n\n/\n/g' iicalc-arch/iicalc.install

cp -f iicalc.deb "iicalc-arch/iicalc-${versionarr[0]}.deb"

if printf '%s\n' "$@" | grep -q -P '^--headless$|^-h$'; then
  chmod -R 757 iicalc-arch
fi

cd iicalc-arch

# generate SRCINFO
if printf '%s\n' "$@" | grep -q -P '^--headless$|^-h$'; then
  sudo -u nobody makepkg --printsrcinfo > .SRCINFO
else
  makepkg --printsrcinfo > .SRCINFO
fi
makepkg -s

rm -rf "iicalc-${versionarr[0]}.deb" pkg/ src/

mv *.pkg* ../iicalc-any.pkg.tar.zst

exit 0