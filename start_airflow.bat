@echo off
:: Fix QuickEdit: disable for all future CMD windows (prevents accidental click-pause)
reg add "HKCU\Console" /v QuickEdit /t REG_DWORD /d 0 /f >nul 2>&1
:: Fix stdin: < nul isolates WSL stdin so docker-compose exec never blocks on Windows console
wsl --cd "%~dp0" bash start.sh < nul
pause
