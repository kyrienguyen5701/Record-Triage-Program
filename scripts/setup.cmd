@Echo off
set root_dir=..
set app_dir=%root_dir%\app
SET folder=%~dp0..\

@echo off
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%userprofile%\Desktop\Triage Program.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%folder%\app\main.cmd%" >> CreateShortcut.vbs
echo oLink.Description = "Triage V2.1" >> CreateShortcut.vbs
echo oLink.IconLocation = "%folder%\app\assets\icon.ico" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

set /p APIKey="Enter your Alma API key: "
@echo off
echo ALMA_API_KEY=%APIKey% > %app_dir%\src\.env && IF EXIST %app_dir%\src\sample.env (@DEL %app_dir%\src\sample.env)
echo Writing API key ...

echo Installing requirements ...
pip install -r %root_dir%\requirements.txt

echo Creating logging directory ...
mkdir %app_dir%\logs

echo Creating output directory ...
mkdir %app_dir%\outputs

echo Now you can close this window and run main.cmds
pause
