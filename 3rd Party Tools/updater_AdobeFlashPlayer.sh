#!/bin/bash

outDir=~/3rd\ Party\ Tools
# if the tools directory doesn't exist, create it
if [ ! -d "$outDir" ]
then
  mkdir "$outDir"
fi
# download Adobe Flash Player and build the package
autopkg run ~/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/AdobeFlashPlayer/AdobeFlashPlayer.pkg.recipe
# move the built pkg to outDir
fileName=$(basename ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.FlashPlayerExtractPackage/AdobeFlashPlayer-*.pkg)
mv ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.FlashPlayerExtractPackage/"$fileName" "$outDir"/"$fileName"
# Remove leftover directories and files
rm -rf ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.FlashPlayerExtractPackage
echo "Adobe Flash Player installer at $outDir/$fileName"
