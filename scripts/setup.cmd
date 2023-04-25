@Echo off
set root_dir=..
set app_dir=%root_dir%\app

echo Installing requirements ...
pip install -r %root_dir%\requirements.txt

echo Creating logging directory ...
mkdir %app_dir%\logs

echo Creating output directory ...
mkdir %app_dir%\outputs

echo Now you can close this window and run main.cmd
pause
