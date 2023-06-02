@Echo off
set RepoOwner=schaffer-library
set RepoName=Record-Triage-Program-main
set RepoDir=%TmpDir%\%RepoName%
set SrcDir=%RepoDir%\app
set TgtDir=%~dp0..\app

set BackupVersion=0
set BackupDir=%~dp0..\backup_version0

:while_exist_old_backup
IF EXIST %BackupDir% (
  set /a BackupVersion+=1
  set BackupDir=%~dp0..\backup_version%BackupVersion%
  goto :while_exist_old_backup
)

echo Creating backup at %BackupDir%...
xcopy /s /e /h /i /y %TgtDir% %BackupDir%

set CacheDir=%~dp0..\.cache
set TmpDir=%CacheDir%\tmp

IF NOT EXIST %CacheDir% (
  mkdir %CacheDir%
  mkdir %TmpDir%
)

set TmpZipFn=%TmpDir%\source.zip
set ZipFn=%CacheDir%\source.zip

echo Downloading from source ...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12, [Net.SecurityProtocolType]::Tls11, [Net.SecurityProtocolType]::Ssl3, [Net.SecurityProtocolType]::Tls; Invoke-WebRequest -Uri 'https://github.com/%RepoOwner%/Record-Triage-Program/archive/refs/heads/main.zip' -OutFile '%TmpZipFn%';}"

IF NOT EXIST %ZipFn% (
  move %TmpZipFn% %CacheDir%
) ELSE (
  :: do sth to check if two files are different later
  move %TmpZipFn% %CacheDir%
)

echo Unzipping ...
powershell -command "Expand-Archive -Force '%ZipFn%' '%TmpDir%'"

xcopy /s /e /h /i /y %SrcDir% %TgtDir%

rmdir /Q /S %RepoDir%
pause
