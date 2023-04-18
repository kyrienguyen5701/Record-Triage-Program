@Echo off

:: Cache current directory
:: set cur_dir="%~dp0"

:: Elevating UAC Administrator Privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if "%errorlevel%" NEQ "0" (
	echo: Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
	echo: UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
	"%temp%\getadmin.vbs" &	exit 
)
if exist "%temp%\getadmin.vbs" del /f /q "%temp%\getadmin.vbs"

:: Configuration for installing
set py_version=3.8.0
set installer="%userprofile%\Downloads\python-%py_version%.exe"
set install_dir="%userprofile%\AppData\Local\Programs\Python\Python_%py_version%"
set install_path="%userprofile%\AppData\Local\Programs\Python\Python_%py_version%\python.exe"

:: Download the installer if not found
IF EXIST %installer% (
  echo [32mFound Python %py_version% Installer at %installer%[0m
) ELSE (
  :: winget install Python.Python.%py_version% -l %install_dir%
  echo [33mCannot find Python %py_version% Installer at %installer%, begin downloading installer ...[0m
  powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12, [Net.SecurityProtocolType]::Tls11, [Net.SecurityProtocolType]::Ssl3, [Net.SecurityProtocolType]::Tls; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/%py_version%/python-%py_version%-amd64.exe' -OutFile '%installer%';}"
)

:: Install Python if not found
IF EXIST %install_path% (
  echo [32mFound Python %py_version% at %install_path%[0m
) ELSE (
  echo [33mCannot find Python %py_version% at %install_path%, begin installing ...[0m
  powershell %installer% InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=%install_dir%
)

:: Install dependencies
:: cd %cur_dir%
:: pip install -r requirements.txt

echo Follow the Python Installer and wait for it to finish to installing, then run setup.cmd
pause
