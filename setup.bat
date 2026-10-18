@echo off

if not exist init.bat (
    echo Downloading init.bat...
    curl -O --ssl-no-revoke https://openhutb.github.io/init.bat
    init.bat
)

if not exist serve.bat (
    echo Downloading serve.bat...
    curl -fsSL -o serve.bat --ssl-no-revoke https://raw.githubusercontent.com/OpenHUTB/template/refs/heads/master/serve.bat
)
echo Calling serve.bat...
call serve.bat


