@echo off

REM Set the working directory to the script's location
cd /d "%~dp0"

REM Check if main.exe exists
if not exist scripts/create/main.exe (
    echo Compiling main.c into main.exe...
    gcc scripts/create/main.c -o scripts/create/main.exe -lm
    if %ERRORLEVEL% neq 0 (
        echo Compilation failed!
        exit /b %ERRORLEVEL%
    )
) else (
    echo main.exe already exists. Skipping compilation.
)

REM Run the executable
echo Running main.exe...
"%~dp0scripts\create\main.exe"
if %ERRORLEVEL% neq 0 (
    echo main.exe failed!
    exit /b %ERRORLEVEL%
)

REM Run converter.py
echo Running scripts/cogs/converter.py...
python scripts/cogs/converter.py
if %ERRORLEVEL% neq 0 (
    echo converter.py failed!
    exit /b %ERRORLEVEL%
)

REM Check if FFmpeg is installed
echo Checking for FFmpeg...
ffmpeg -version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: FFmpeg is not installed or not in PATH!
    exit /b 1
)

REM Convert PNG files in the images folder to a video
echo Creating video from PNG files in the images folder...
if not exist images (
    echo Error: images folder does not exist!
    exit /b 1
)

ffmpeg -framerate 30 -i images/frame_%%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4
if %ERRORLEVEL% neq 0 (
    echo Failed to create video from PNG files!
    exit /b %ERRORLEVEL%
)

REM Clean up files
echo Cleaning up PNG files...
python scripts/cogs/cleaner.py
if %ERRORLEVEL% neq 0 (
    echo cleanup.py failed!
    exit /b %ERRORLEVEL%
)

REM Moving the output video to the videos folder
echo Moving output.mp4 to videos folder...
if not exist videos (
    mkdir videos
)

python scripts/cogs/mover.py
if %ERRORLEVEL% neq 0 (
    echo mover.py failed!
    exit /b %ERRORLEVEL%
)

echo All tasks completed successfully!
pause