#!/bin/bash

#################################
#
# This script requires the path of the lame dmg to be passed as the first parameter
#
#################################

if [ ! "$1" ]
then
  echo "Please pass the path to the Jing dmg file as the first parameter..."
  exit 1
fi

outDir=~/3rd\ Party\ Tools
# if the tools directory doesn't exist, create it
if [ ! -d "$outDir" ]
then
  mkdir "$outDir"
fi

# mount the dmg that was passed to the script.
hdiutil attach "$1" -nobrowse -quiet
volpath=/Volumes/"$(ls /Volumes/ | grep 'Jing')"
fileName=$(basename "$volpath"/*.app)

# verify that the dmg is for Lame and has a pkg in it
if [ ! -d "$volpath"/"$fileName" ]
then
  echo "Could not find Lame at:"
  echo "$fileName"
  echo "May need to update script to match name format..."
  exit 1
fi

#get identifier and version
identifier=$(/usr/libexec/PlistBuddy -c 'Print CFBundleIdentifier' "$volpath"/Jing.app/Contents/Info.plist)
version=$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' "$volpath"/Jing.app/Contents/Info.plist)

# build pkg
pkgbuild --component "$volpath"/Jing.app --version "$version" --identifier "$identifier" --install-location /Applications "$outDir"/Jing-"$version".pkg

#unmount dmg
hdiutil detach "$volpath"

echo "Jing installer at $outDir/Jing-$version.pkg"
