#!/bin/bash

outDir=~/3rd\ Party\ Tools
# if the tools directory doesn't exist, create it
if [ ! -d "$outDir" ]
then
  mkdir "$outDir"
fi
# download Skype and build the package
autopkg run ~/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/Skype/Skype.pkg.recipe
# move the built pkg to outDir
fileName=$(basename ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.Skype/Skype-*.pkg)
mv ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.Skype/"$fileName" "$outDir"/"$fileName"
# Remove leftover directories and files
rm -rf ~/Library/AutoPkg/Cache/com.github.autopkg.pkg.Skype
echo "Skype installer at $outDir/$fileName"
