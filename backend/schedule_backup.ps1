$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

& .\venv\Scripts\python.exe .\backup_db.py
