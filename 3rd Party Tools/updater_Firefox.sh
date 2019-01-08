#!/bin/bash

outDir=~/3rd\ Party\ Tools
# if the tools directory doesn't exist, create it
if [ ! -d "$outDir" ]
then
  mkdir "$outDir"
fi
# download Firefox.dmg
autopkg run ~/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/Mozilla/Firefox.download.recipe
# mount the Firefox dmg
hdiutil attach ~/Library/AutoPkg/Cache/com.github.autopkg.download.firefox-rc-en_US/downloads/Firefox.dmg -nobrowse -quiet
# copy Firefox.app to our 3rd party working direcotry
cp -R /Volumes/Firefox/Firefox.app "$outDir"/Firefox.app
# unmount the Firefox dmg
hdiutil detach /Volumes/Firefox
# unquarantine Firefox app
xattr -r -d com.apple.quarantine "$outDir"/Firefox.app
# Retrieve the bundle identifier
identifier=$(/usr/libexec/PlistBuddy -c 'Print CFBundleIdentifier' "$outDir"/Firefox.app/Contents/Info.plist)
# Retrieve the version we are working with
version=$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' "$outDir"/Firefox.app/Contents/Info.plist)
# Write the customization files into the app
cat <<EOM >"$outDir"/Firefox.app/Contents/Resources/defaults/pref/autoconfig.js
// Any comment. You must start the file with a comment!
pref("general.config.filename", "mozilla.cfg");
pref("general.config.obscure_value", 0);
EOM
cat <<EOM >"$outDir"/Firefox.app/Contents/Resources/mozilla.cfg
// Mozilla Firefox Mozilla.cfg

// Disable updater
lockPref("app.update.enabled", false);
// make absolutely sure it is really off
lockPref("app.update.auto", false);
lockPref("app.update.mode", 0);
lockPref("app.update.service.enabled", false);

// Disable Add-ons compatibility checking
clearPref("extensions.lastAppVersion");

// Don't show 'know your rights' on first run
pref("browser.rights.3.shown", true);

// Don't show WhatsNew on first run after every update
pref("browser.startup.homepage_override.mstone","ignore");

// Set default homepage - users can change
// Requires a complex preference
defaultPref("browser.startup.homepage","data:text/plain,browser.startup.homepage=https://myau.ashland.edu");
pref("browser.startup.homepage_override.buildID", "20120420145725");
pref("browser.startup.homepage_override.mstone", "ignore");

// Disable the internal PDF viewer
pref("pdfjs.disabled", true);

// Disable the flash to javascript converter
pref("shumway.disabled", true);

// Don't ask to install the Flash plugin
pref("plugins.notifyMissingFlash", false);

//Disable plugin checking
lockPref("plugins.hide_infobar_for_outdated_plugin", true);
clearPref("plugins.update.url");

// Disable health reporter
lockPref("datareporting.healthreport.service.enabled", false);

// Disable all data upload (Telemetry and FHR)
lockPref("datareporting.policy.dataSubmissionEnabled", false);

// Disable crash reporter
lockPref("toolkit.crashreporter.enabled", false);
Components.classes["@mozilla.org/toolkit/crash-reporter;1"].getService(Components.interfaces.nsICrashReporter).submitReports = false;

pref("browser.anchor_color", "#0000FF");
pref("browser.bookmarks.restore_default_bookmarks", false);
pref("browser.cache.disk.capacity", 1048576);
pref("browser.cache.disk.smart_size.first_run", false);
pref("browser.cache.disk.smart_size_cached_value", 880640);
pref("browser.display.background_color", "#C0C0C0");
pref("browser.display.use_system_colors", true);
pref("browser.migration.version", 6);
pref("browser.places.smartBookmarksVersion", 2);
pref("browser.preferences.advanced.selectedTabIndex", 0);
pref("browser.rights.3.shown", true);
pref("browser.search.update", false);
pref("browser.shell.checkDefaultBrowser", false);
pref("browser.tabs.warnOnClose", true);
pref("browser.visited_color", "#800080");
pref("browser.search.defaultenginename", "Google");
pref("browser.search.defaultenginename.US", "data:text/plain,browser.search.defaultenginename.US=Google");
pref("browser.search.order.1", "Google");
pref("browser.search.order.2", "Yahoo");
pref("browser.search.order.US.1", "data:text/plain,browser.search.order.US.1=Google");
pref("browser.search.order.US.2", "data:text/plain,browser.search.order.US.2=Yahoo");
pref("extensions.pendingOperations", false);
pref("extensions.shownSelectionUI", true);
pref("extensions.update.enabled", false);
pref("privacy.sanitize.migrateFx3Prefs", true);
pref("privacy.sanitize.timeSpan", 0);
pref("signon.rememberSignons", false);
pref("toolkit.telemetry.prompted", 2);
pref("toolkit.telemetry.rejected", true);
pref("browser.disableResetPrompt", true);
EOM
# Build the installer package to be deployed
pkgbuild --component "$outDir"/Firefox.app --version "$version" --identifier "$identifier" --install-location /Applications "$outDir"/Firefox-"$version".pkg
# Remove leftover directories and files
rm -rf ~/Library/AutoPkg/Cache/com.github.autopkg.download.firefox-rc-en_US
rm -rf "$outDir"/Firefox.app
echo "Firefox installer at $outDir/Firefox-$version.pkg"
