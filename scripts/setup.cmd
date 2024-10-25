@Echo off
set root_dir=..
set app_dir=%root_dir%\app
set folder=%~dp0..\

@echo off
IF EXIST %app_dir%\src\.env (
    echo API Key located ...
) ELSE (
set /p APIKey="Enter your Alma API key: "
call echo ALMA_API_KEY=%%APIKey%% > %app_dir%\src\.env && IF EXIST %app_dir%\src\sample.env (@DEL %app_dir%\src\sample.env)
echo Writing API key ...
echo:
)


:: Creates a vb executable to create .lnk file on the desktop
@echo off
IF EXIST %userprofile%\Desktop\Triage Program.lnk (
    echo Desktop Shortcut Located ...
    echo:
) ELSE (
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%userprofile%\Desktop\Triage Program.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%folder%\app\main.cmd%" >> CreateShortcut.vbs
echo oLink.Description = "Triage V2.1" >> CreateShortcut.vbs
echo oLink.IconLocation = "%folder%\app\src\assets\icon.ico" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs
)

echo Installing requirements ...
pip install -r %root_dir%\requirements.txt

echo:
echo Creating logging directory ...
mkdir %app_dir%\logs

echo:
echo Creating output directories ...
:: Debugging outputs
mkdir %app_dir%\outputs
:: User outputs
mkdir "%userprofile%\Desktop\Triage Outputs"

echo:
echo Now you can close this window and run main.cmds
pause
