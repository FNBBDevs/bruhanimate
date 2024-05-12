@echo off

echo Waiting for 5 seconds before folder delete.
timeout /t 5 /nobreak >nul

setlocal enabledelayedexpansion
set "folders=.eggs build bruhanimate.egg-info dist"

for %%i in (%folders%) do (
    if exist %%i (
        ren %%i "temp" >nul 2>&1
        if errorlevel 1 (
            echo Folder %%i is in use.
        ) else (
            ren "temp" %%i >nul 2>&1
            rmdir /s /q %%i
            echo Folder %%i removed.
            timeout /t 1 /nobreak >nul
        )
    ) else (
        echo Folder %%i not found.
    )
)

echo Starting publish.
echo Pushing version number
python push_version.py
echo Running setup.py
python setup.py sdist bdist >nul
echo Uploading to pypi
twine upload dist/* -u %pypi-username% -p %pypi-password%

echo Pushing to Github.
git add .
git commit -m "version bump"
git push

echo Publish complete.
