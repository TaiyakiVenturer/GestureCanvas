@echo off
chcp 950 > nul

echo === Python�������ҳ]�m�}�� ===
echo.

REM �ˬdPython 3.12�O�_�i��
py -3.12 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [���~] �����Python 3.12�A�нT�O�w�w��Python 3.12
    echo        �ФU���æw��Python 3.12�Ghttps://www.python.org/downloads/
    pause
    exit /b 1
)

REM ��ܨϥΪ�Python����
echo [�H��] �ϥ�Python�����G
py -3.12 --version

REM �ˬd�������ҬO�_�s�b
set VENV_DIR=.venv
if exist %VENV_DIR%\Scripts\python.exe (
    echo [�H��] �ϥβ{����������
) else (
    echo [�H��] �ϥ�Python 3.12�Ыطs��������...
    py -3.12 -m venv %VENV_DIR%
    if %errorlevel% neq 0 (
        echo [���~] �������ҳЫإ���
        pause
        exit /b 1
    )
)

REM �Ұʵ�������
echo [�H��] �Ұʵ�������...
call %VENV_DIR%\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [���~] �������ұҰʥ���
    pause
    exit /b 1
)

REM �ˬdrequirements.txt�O�_�s�b
if not exist requirements.txt (
    echo [���~] requirements.txt���s�b
    pause
    exit /b 1
)

REM ��spip
echo [�H��] ��spip...
python -m pip install --upgrade pip

REM �w�ˮM��
echo [�H��] �w�˥��n�M��...
pip install -r requirements.txt

REM ��ܤw�w�˪��M��
echo.
echo === �w�w�˪��M�� ===
pip list

echo.
echo =====================================
echo [����] �]�m�����A�������Ҥw�ҰʡA��Jdeactivate�i�h�X
echo =====================================

pause
