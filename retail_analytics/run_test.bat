@echo off
echo Running Phase 2 System Test...
echo.

REM Change to the correct directory
cd /d d:\codebuddy\education\retail_analytics

REM Run the test script using Python directly
python test_phase2_complete.py

echo.
echo Test completed.
pause
