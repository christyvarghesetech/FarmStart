"""
FarmStart Backend Runner Script
Starts the FastAPI server with hot-reloading on port 8000.
"""

import os
import sys
import uvicorn

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("Starting FarmStart (New Farmer Copilot) Backend API...")
    print("API Documentation available at: http://127.0.0.1:8000/docs")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
