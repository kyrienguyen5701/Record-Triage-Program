@Echo off
set CacheDir=%~dp0..\.cache
set TmpDir=%CacheDir%\tmp

IF NOT EXIST %CacheDir% (
  mkdir %CacheDir%
  mkdir %TmpDir%
)

set TmpZipFn=%TmpDir%\source.zip
set ZipFn=%CacheDir%\source.zip

echo Downloading from source ...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12, [Net.SecurityProtocolType]::Tls11, [Net.SecurityProtocolType]::Ssl3, [Net.SecurityProtocolType]::Tls; Invoke-WebRequest -Uri 'https://github.com/kyrienguyen5701/Record-Triage-Program/archive/refs/heads/main.zip' -OutFile '%TmpZipFn%';}"

IF NOT EXIST %ZipFn% (
  move %TmpZipFn% %CacheDir%
) ELSE (
  :: do sth to check if two files are different later
  move %TmpZipFn% %CacheDir%
)

echo Unzipping ...
powershell -command "Expand-Archive -Force '%ZipFn%' '%TmpDir%'"

set RepoName=Record-Triage-Program-main
set RepoDir=%TmpDir%\%RepoName%
set SrcDir=%RepoDir%\app
set TgtDir=%~dp0..\app

:: Temporary Hack
move %SrcDir%\* %TgtDir%
move %SrcDir%\src\* %TgtDir%\src


rmdir /Q /S %RepoDir%
pause
