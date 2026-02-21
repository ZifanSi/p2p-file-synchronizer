@echo off
setlocal EnableExtensions EnableDelayedExpansion

set PORTS=9000 8000 8001 8002 8003 8004 8005 8006 8007 8008 8009 

for %%P in (%PORTS%) do (
  echo.
  echo === Port %%P ===
  for /f "tokens=5" %%A in ('netstat -ano ^| findstr /R /C:":%%P .*LISTENING"') do (
    echo Killing PID %%A on port %%P
    taskkill /PID %%A /F >nul 2>nul
  )
)

echo.
echo Done.
pause