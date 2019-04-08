#!/bin/bash

#################################
#
# This script requires the path of the lame dmg to be passed as the first parameter
#
#################################

if [ ! "$1" ]
then
  echo "Please pass the path to the lame dmg file as the first parameter..."
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
volpath=/Volumes/"$(ls /Volumes/ | grep 'Lame Library*')"
fileName=$(basename "$volpath"/*.pkg)

# verify that the dmg is for Lame and has a pkg in it
if [ ! -f "$volpath"/"$fileName" ]
then
  echo "Could not find Lame at:"
  echo "$fileName"
  echo "May need to update script to match name format..."
  exit 1
fi

# get and version
version=$(basename "$volpath"/*.pkg | sed -e 's/Lame Library v\(.*\) for Audacity.pkg/\1/')

# copy pkg to our working directory
cp "$volpath"/"$fileName" "$outDir"/Lame-"$version".pkg

#unmount dmg
hdiutil detach "$volpath"

echo "Lame installer at $outDir/Lame-$version.pkg"
