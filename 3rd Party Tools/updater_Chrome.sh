#!/bin/bash

outDir=~/3rd\ Party\ Tools
# if the tools directory doesn't exist, create it
if [ ! -d "$outDir" ]
then
  mkdir "$outDir"
fi
# download GoogleChrome and build the package
autopkg run ~/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/GoogleChrome/GoogleChrome.pkg.recipe
# move the built pkg to outDir
fileName=$(basename ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.googlechrome/GoogleChrome-*.pkg)
mv ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.googlechrome/"$fileName" "$outDir"/"$fileName"
# Remove leftover directories and files
rm -rf ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.googlechrome
echo "Chrome installer at $outDir/$fileName"
