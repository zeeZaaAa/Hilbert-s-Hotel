#เอาไว้รัน frontend + backend พร้อมกัน
import subprocess
import os
import sys

# เข้า root folder ของโปรเจกต์
root_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(root_path)

# รัน backend
subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"])

# รัน frontend
subprocess.Popen([sys.executable, "-m", "uvicorn", "mookmeh.frontend.app:app", "--reload", "--port", "3000"])

print("Backend + Frontend running...")
