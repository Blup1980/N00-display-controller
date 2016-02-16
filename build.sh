#!/bin/bash

mkdir -p build/usr/share/N00-display-controller/
mkdir -p build/etc/
mkdir -p build/DEBIAN/
rsync --exclude .idea -aR ./src/ build/usr/share/N00-display-controller/
rsync --exclude .idea -aR ./etc/ build/
rsync -a debianScripts/ build/DEBIAN

sudo dpkg-deb --build build N00-display-controller.deb

rm -rf ./build
