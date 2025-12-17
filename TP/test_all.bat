@echo off
REM Test script for the Triangulator project

echo.
echo ========================================
echo TRIANGULATOR PROJECT VERIFICATION
echo ========================================
echo.

echo [1/3] Checking lint...
python -m ruff check .
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Lint check failed
    goto error
)
echo PASS: Lint check
echo.

echo [2/3] Running unit tests...
python -m pytest tests/ -m "not performance" -q
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Unit tests failed
    goto error
)
echo PASS: Unit tests
echo.

echo [3/3] Running performance tests...
python -m pytest tests/ -m "performance" -q
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Performance tests failed
    goto error
)
echo PASS: Performance tests
echo.

echo ========================================
echo ALL TESTS PASSED!
echo ========================================
exit /b 0

:error
echo ========================================
echo TEST FAILED
echo ========================================
exit /b 1
