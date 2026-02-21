@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem Ports to kill (tracker + peers)
set PORTS=9000 8000 8001 8002 8003 8004 8005 8006 8007 8008 8009

for %%P in (%PORTS%) do (
  echo.
  echo === Port %%P ===
  for /f "tokens=5" %%A in ('netstat -ano ^| findstr /R /C:":%%P .*LISTENING"') do (
    set PID=%%A
    for /f "tokens=1,*" %%i in ('tasklist /FI "PID eq !PID!" /FO CSV /NH') do set PROC=%%~i

    if /I "!PROC!"=="python.exe" (
      echo Killing python PID !PID! on port %%P
      taskkill /PID !PID! /F >nul 2>nul
    ) else if /I "!PROC!"=="pythonw.exe" (
      echo Killing pythonw PID !PID! on port %%P
      taskkill /PID !PID! /F >nul 2>nul
    ) else (
      echo Skipping PID !PID! (process !PROC!)
    )
  )
)

echo.
echo Done.
pause