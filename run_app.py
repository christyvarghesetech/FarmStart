"""
FarmStart Unified Launcher
Run from repository root: python run_app.py
"""
import os
import sys
import uvicorn

if __name__ == "__main__":
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    sys.path.insert(0, backend_dir)
    os.chdir(backend_dir)
    print("================================================================")
    print("  FarmStart - New Farmer Copilot (AI Conclave 2026)")
    print("  Application URL: http://127.0.0.1:8000/app/")
    print("  API Docs (Swagger): http://127.0.0.1:8000/docs")
    print("================================================================")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
