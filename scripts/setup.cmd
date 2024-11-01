@Echo off

set root_dir=..
set app_dir=%root_dir%\app
set folder=%~dp0..\

IF EXIST %app_dir%\src\.env (
    echo API Key located ...
) ELSE (
set /p APIKey="Enter your Alma API key: "
call echo ALMA_API_KEY=%%APIKey%% > %app_dir%\src\.env && IF EXIST %app_dir%\src\sample.env (@DEL %app_dir%\src\sample.env)
echo Writing API key ...
echo:
)

echo Installing requirements ...
python -m pip install --upgrade pip
pip install -r %root_dir%\requirements.txt

echo:
echo Creating logging directory ...
mkdir %app_dir%\logs

echo:
echo Creating output directories ...
:: Debugging outputs
mkdir %app_dir%\outputs

echo:
echo Press enter to select a location for Program Icon:
pause>Nul
python src\select_dir.py > %app_dir%\src\assets\homeDir.txt
set /p IconDir=<%app_dir%\src\assets\homeDir.txt

:: Default if userdoes not select a file in explorer
IF "%IconDir%"=="C:\" set IconDir=%userprofile%\Desktop

set Shortcut="%iconDir%\Triage Program.lnk"

:: Creates a vb executable to create .lnk file on the desktop
IF EXIST "%Shortcut%" (
    echo Desktop Shortcut Located ...
    echo:
) ELSE (
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = %Shortcut% >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%folder%\app\main.cmd%" >> CreateShortcut.vbs
echo oLink.Description = "Triage V2.1.3" >> CreateShortcut.vbs
echo oLink.IconLocation = "%folder%\app\src\assets\icon.ico" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs>Nul
del CreateShortcut.vbs
)

:: User outputs
IF NOT EXIST "%IconDir%\Triage Outputs" mkdir "%IconDir%\Triage Outputs"

echo Now you can close this window and run main.cmd
pause
