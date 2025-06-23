@echo off
chcp 950 > nul

echo === Python虛擬環境設置腳本 ===
echo.

REM 檢查Python 3.12是否可用
py -3.12 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [錯誤] 未找到Python 3.12，請確保已安裝Python 3.12
    echo        請下載並安裝Python 3.12：https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 顯示使用的Python版本
echo [信息] 使用Python版本：
py -3.12 --version

REM 檢查虛擬環境是否存在
set VENV_DIR=.venv
if exist %VENV_DIR%\Scripts\python.exe (
    echo [信息] 使用現有虛擬環境
) else (
    echo [信息] 使用Python 3.12創建新虛擬環境...
    py -3.12 -m venv %VENV_DIR%
    if %errorlevel% neq 0 (
        echo [錯誤] 虛擬環境創建失敗
        pause
        exit /b 1
    )
)

REM 啟動虛擬環境
echo [信息] 啟動虛擬環境...
call %VENV_DIR%\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [錯誤] 虛擬環境啟動失敗
    pause
    exit /b 1
)

REM 檢查requirements.txt是否存在
if not exist requirements.txt (
    echo [錯誤] requirements.txt不存在
    pause
    exit /b 1
)

REM 更新pip
echo [信息] 更新pip...
python -m pip install --upgrade pip

REM 安裝套件
echo [信息] 安裝必要套件...
pip install -r requirements.txt

REM 顯示已安裝的套件
echo.
echo === 已安裝的套件 ===
pip list

echo.
echo =====================================
echo [完成] 設置完成，虛擬環境已啟動，輸入deactivate可退出
echo =====================================

pause
