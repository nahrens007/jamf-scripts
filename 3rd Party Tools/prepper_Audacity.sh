#!/bin/bash

#################################
#
# This script requires the path of the audacity dmg to be passed as the first parameter
#
#################################

if [ ! "$1" ]
then
  echo "Please pass the path to the Audacity dmg file as the first parameter..."
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
volpath=/Volumes/"$(ls /Volumes/ | grep 'Audacity')"

# verify that the dmg is for Audacity
if [ ! -d "$volpath"/Audacity.app ]
then
  echo "Could not find Audacity.app at:"
  echo "$volpath"/Audacity.app
  exit 1
fi

#get identifier and version
identifier=$(/usr/libexec/PlistBuddy -c 'Print CFBundleIdentifier' "$volpath"/Audacity.app/Contents/Info.plist)
version=$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' "$volpath"/Audacity.app/Contents/Info.plist)

# build pkg
pkgbuild --component "$volpath"/Audacity.app --version "$version" --identifier "$identifier" --install-location /Applications "$outDir"/Audacity-"$version".pkg

#unmount dmg
hdiutil detach "$volpath"

echo "Audacity installer at $outDir/Audacity-$version.pkg"
