@Echo off
set root_dir=..
set app_dir=%root_dir%\app

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

echo Now you can close this window and run main.cmd
pause
