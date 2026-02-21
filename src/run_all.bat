@echo off
set IP=127.0.0.1
set PORT=9000

cd /d %~dp0

start "TRACKER" cmd /k "python tracker.py %IP% %PORT%"

timeout /t 1 >nul

start "PEER1" cmd /k "cd /d %~dp0Peer1 && python ..\fileSynchronizer.py %IP% %PORT%"
start "PEER2" cmd /k "cd /d %~dp0Peer2 && python ..\fileSynchronizer.py %IP% %PORT%"
start "PEER3" cmd /k "cd /d %~dp0Peer3 && python ..\fileSynchronizer.py %IP% %PORT%"