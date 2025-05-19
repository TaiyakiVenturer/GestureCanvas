@echo off
chcp 65001 > nul

echo === Python虛擬環境設置腳本 ===
echo.

REM 檢查Python是否安裝
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [錯誤] 未找到Python，請確保Python已安裝且加入PATH
    pause
    exit /b 1
)

REM 檢查虛擬環境是否存在
set VENV_DIR=.venv
if exist %VENV_DIR%\Scripts\python.exe (
    echo [信息] 使用現有虛擬環境
) else (
    echo [信息] 創建新虛擬環境...
    python -m venv %VENV_DIR%
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
