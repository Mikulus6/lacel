REM # Install pyinstaller and execute its command. (pip is required)
pip install pyinstaller
pyinstaller --onefile lac.py

REM # Delete unnecessary files created by pyinstaller.
del lac.exe
move dist\lac.exe
del /Q /s build
rmdir /Q /s build
del /Q /s dist
rmdir /Q /s dist
del lac.spec

REM # Wait indefinitely in order to avoid unexpected command-line window disappearance.
timeout -1
