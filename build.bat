@echo off
cd /d "%~dp0"
echo Creating EXE file...

:: Remove old build and dist folders
rmdir /s /q build
rmdir /s /q dist
del main.spec

:: Run PyInstaller with required options
pyinstaller --onefile --icon=1.png ^
  --hidden-import=mariadb ^
  --hidden-import=sqlite3 ^
  --hidden-import=pymysql ^
  --hidden-import=mysql.connector ^
  --collect-all mysql.connector ^
  --add-binary "C:\Program Files\MySQL\MySQL Server 8.0\lib\libmysql.dll;." ^
  --add-binary "C:\Program Files\MySQL\MySQL Server 8.0\lib\plugin;plugin" ^
  main.py
:: Copy config.json and CW.png to the dist folder
echo Copying config.json and CW.png to dist folder...
xcopy /y config.json dist\
xcopy /y CW.png dist\

echo Build complete. EXE file is in the 'dist' folder.
pause
