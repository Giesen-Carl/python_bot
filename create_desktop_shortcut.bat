@echo off
setlocal

:: Folder where this script is located
set "BASE=%~dp0"

:: Relative files
set "TARGET_BAT=%BASE%start_bot.bat"
set "ICON_FILE=%BASE%icon.ico"

:: Shortcut name
set "SHORTCUT_NAME=clash_bot"

:: Create VBS file
set "VBS_SCRIPT=%TEMP%\CreateShortcut.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_SCRIPT%"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\%SHORTCUT_NAME%.lnk" >> "%VBS_SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_SCRIPT%"
echo oLink.TargetPath = "%TARGET_BAT%" >> "%VBS_SCRIPT%"
echo oLink.WorkingDirectory = "%BASE%" >> "%VBS_SCRIPT%"
echo oLink.IconLocation = "%ICON_FILE%" >> "%VBS_SCRIPT%"
echo oLink.Save >> "%VBS_SCRIPT%"

cscript //nologo "%VBS_SCRIPT%"

del "%VBS_SCRIPT%"

echo Desktop shortcut created successfully.
pause