@echo off
setlocal EnableExtensions

rem This bat file lives in src\bats. Go to src.
set "SRC_DIR=%~dp0.."
pushd "%SRC_DIR%" >nul || (echo Failed to cd to "%SRC_DIR%" & exit /b 1)

echo Cleaning Peer folders in: %CD%

del /q Peer1\fileB.txt Peer1\fileC.txt Peer1\big.bin Peer1\*.part 2>nul
del /q Peer2\fileA.txt Peer2\fileC.txt Peer2\big.bin Peer2\*.part 2>nul
del /q Peer3\fileA.txt Peer3\fileB.txt Peer3\big.bin Peer3\*.part 2>nul

echo Done.
popd >nul
pause