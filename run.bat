@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting server at http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python server.py