@echo off

start "Backend" cmd /k "cd /d C:\Users\olegk\Desktop\Tuke\2025-2026 tuke\BP\backend && python -m uvicorn main:app --reload --port 8000"
start "Frontend" cmd /k "cd /d C:\Users\olegk\Desktop\Tuke\2025-2026 tuke\BP\frontend && npm run serve"
