@echo off
echo ========================================
echo  TriVenta Tech Ltd - GitHub Deployment
echo ========================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/windows
    echo Then restart this script.
    pause
    exit /b 1
)

echo Git detected. Proceeding with deployment...
echo.

REM Initialize repository if needed
if not exist .git (
    echo Initializing Git repository...
    git init
    git remote add origin https://github.com/RahasoftBwire/TriVentaTechLTD.git
)

echo Adding all files...
git add .

echo.
set /p commit_message="Enter commit message (or press Enter for default): "
if "%commit_message%"=="" set commit_message="Website update - %date% %time%"

echo Committing changes...
git commit -m "%commit_message%"

echo.
echo Pushing to GitHub...
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo  SUCCESS! Website deployed to GitHub
    echo ========================================
    echo.
    echo Your website will be live at:
    echo https://rahasoftbwire.github.io/TriVentaTechLTD/
    echo.
    echo It may take a few minutes for changes to appear.
) else (
    echo.
    echo ========================================
    echo  DEPLOYMENT FAILED
    echo ========================================
    echo.
    echo Please check your internet connection and GitHub credentials.
    echo You may need to configure Git with your credentials:
    echo   git config --global user.name "Your Name"
    echo   git config --global user.email "your.email@example.com"
)

echo.
pause