@echo off
chcp 65001 >nul
echo ================================================
echo Aim Lab 练枪模拟器 - 快速启动
echo ================================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo [1/3] 检查 Python 版本...
python --version

echo.
echo [2/3] 安装依赖...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo.
echo [3/3] 启动游戏...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo [错误] 游戏运行出错
    pause
)
