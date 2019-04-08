#!/bin/bash

outDir=~/3rd\ Party\ Tools
# if the tools directory doesn't exist, create it
if [ ! -d "$outDir" ]
then
  mkdir "$outDir"
fi
# download and build pkg
autopkg run ~/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/AdobeReader/AdobeReaderDC.pkg.recipe
# move the built pkg to outDir
fileName=$(basename ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.AdobeReaderDC/AcroRdrDC_*.pkg)
version=$(echo $fileName | sed -e 's/AcroRdrDC_\(.*\)_MUI.pkg/\1/')
mv ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.AdobeReaderDC/"$fileName" "$outDir"/AdobeReaderDC-"$version".pkg
# Remove leftover directories and files
rm -rf ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.AdobeReaderDC
echo "Adobe Reader installer at $outDir/AdobeReaderDC-$version.pkg"
