@echo off
:: 设置编码为UTF-8，防止中文路径或提示显示乱码
chcp 65001 >nul
cls

echo =========================================
echo       D2R 同步数据版本编号 国服
echo =========================================
echo.

:: =================【配置区域】=================
set "DOWNLOAD_URL=https://gist.githubusercontent.com/jcymeow/8b259ad1d5f931a8ad058f122b20ed45/raw/af751d161530a77264c36e41f98dfa628c7c1efb/dataversionbuild.txt"
:: ==============================================

:: 【关键修复】将工作目录强制切换到脚本所在的实际目录（C:\...\mods\jcy）
cd /d "%~dp0"

:: 1. 寻找当前目录下第一个以 .mpq 结尾的文件夹
set "TARGET_MPQ="
for /d %%i in (*.mpq) do (
    set "TARGET_MPQ=%%i"
    goto :FOUND
)

:FOUND
:: 检查是否找到了 .mpq 文件夹
if "%TARGET_MPQ%"=="" (
    echo 【错误】在以下目录下没有找到任何 *.mpq 文件夹：
    echo "%CD%"
    echo 请检查脚本是否放在了正确的 MOD 文件夹内。
    goto :END
)

echo [1/3] 找到目标目录: %TARGET_MPQ%

:: 2. 拼接完整的保存路径
set "SAVE_DIR=%TARGET_MPQ%\data\global"
set "SAVE_FILE=%SAVE_DIR%\dataversionbuild.txt"

:: 3. 如果 data\global 目录不存在，则创建（加了 /p 确保多级目录安全创建）
if not exist "%SAVE_DIR%" (
    echo [2/3] 正在创建目标目录: %SAVE_DIR%
    if not exist "%TARGET_MPQ%\data" mkdir "%TARGET_MPQ%\data"
    mkdir "%SAVE_DIR%"
) else (
    echo [2/3] 目标目录已存在，准备覆盖文件...
)

:: 4. 调用系统自带的 curl 下载文件
echo [3/3] 正在从云端下载最新版本文件...
:: 优化了 curl 参数：增加 --connect-timeout 限制超时（防止网络卡死无响应）
curl -s -L -f --connect-timeout 10 "%DOWNLOAD_URL%" -o "%SAVE_FILE%"

:: 5. 检查 curl 的执行结果
if %errorlevel% equ 0 (
    echo.
    echo =========================================
    echo 【成功】版本文件已同步并保存至：
    echo "%SAVE_FILE%"
    echo =========================================
) else (
    echo.
    echo =========================================
    echo 【失败】下载过程中出错，请检查：
    echo 1. 网络连接是否正常（GitHub/Gist 是否能连通）
    echo 2. 如果使用了代理/加速器，请确保命令行能正常走代理
    echo =========================================
)

:END
echo.
echo 按任意键退出...
pause >nul