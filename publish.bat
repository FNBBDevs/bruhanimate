@echo off

setlocal EnableDelayedExpansion

echo Starting publish.

REM Push version number
echo Pushing version number
python push_version.py
IF ERRORLEVEL 1 (
    echo Failed to push version number.
    exit /b 1
)

REM Build the package
echo Building the package
poetry build
IF ERRORLEVEL 1 (
    echo Package build failed.
    exit /b 1
)

REM Check if environment variables are set
if "%pypi-username%"=="" (
    echo PyPI username not set. Please set environment variable pypi-username.
    exit /b 1
)
if "%pypi-password%"=="" (
    echo PyPI password not set. Please set environment variable pypi-password.
    exit /b 1
)

REM Publish to PyPI
echo Publishing to PyPI
poetry publish --username %pypi-username% --password %pypi-password%
IF ERRORLEVEL 1 (
    echo Failed to publish to PyPI.
    exit /b 1
)

REM Commit and push changes to GitHub
echo Pushing to Github.
git add .
git commit -m "version bump"
git push
IF ERRORLEVEL 1 (
    echo Failed to push to GitHub.
    exit /b 1
)

echo Publish complete.

endlocal
