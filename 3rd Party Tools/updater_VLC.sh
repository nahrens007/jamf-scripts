#!/bin/bash

outDir=~/3rd\ Party\ Tools
# if the tools directory doesn't exist, create it
if [ ! -d "$outDir" ]
then
  mkdir "$outDir"
fi
# download VLC and build the package
autopkg run ~/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/VLC/VLC.pkg.recipe
# move the built pkg to outDir
fileName=$(basename ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.VLC/VLC-*.pkg)
mv ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.VLC/"$fileName" "$outDir"/"$fileName"
# Remove leftover directories and files
rm -rf ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.VLC
echo "VLC installer at $outDir/$fileName"
