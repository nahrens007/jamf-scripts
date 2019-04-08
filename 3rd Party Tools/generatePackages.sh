#!/bin/bash

outDir=~/3rd\ Party\ Tools
logFile="$outDir"/packages.log
echo "" > "$logFile"
# These scripts are able to download and package the products automatically
./updater_AdobeFlashPlayer.sh >> "$logFile"
./updater_AdobeReaderDC.sh >> "$logFile"
./updater_Chrome.sh >> "$logFile"
./updater_Firefox.sh >> "$logFile"
./updater_Skype.sh >> "$logFile"
./updater_VLC.sh >> "$logFile"

# These scripts require packages be passed to them
# Audacity https://www.audacityteam.org/download/mac/
# Lame and ffmpeg for Audacity: https://lame.buanzo.org/#lameosxdl
# Jing https://www.techsmith.com/download/jing/
audacityDmg=$(ls "$outDir"/*audacity*.dmg)
ffmpegDmg=$(ls "$outDir"/*ffmpeg*.dmg)
lameDmg=$(ls "$outDir"/*Lame*.dmg)
jingDmg=$(ls "$outDir"/*jing*.dmg)
if [ -f "$audacityDmg" ]
then
  ./prepper_Audacity.sh "$audacityDmg" >> "$logFile"
else
  echo "Audacity's dmg file could not be found."
fi
if [ -f "$ffmpegDmg" ]
then
  ./prepper_ffmpeg.sh "$ffmpegDmg" >> "$logFile"
else
  echo "ffmpeg's dmg file could not be found."
fi
if [ -f "$lameDmg" ]
then
  ./prepper_lame.sh "$lameDmg" >> "$logFile"
else
  echo "Lame's dmg file could not be found."
fi
if [ -f "$jingDmg" ]
then
  ./prepper_jing.sh "$jingDmg" >> "$logFile"
else
  echo "Jing's dmg file could not be found."
fi
