@Echo off
echo Installing requirements ...
pip install -r requirements.txt

echo Creating logging directory ...
mkdir logs

echo Creating output directory ...
mkdir outputs

echo Now you can close this window and run main.cmd
pause
