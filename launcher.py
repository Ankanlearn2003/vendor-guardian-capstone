import subprocess
import sys
import time
import os

print("🚀 Starting VendorGuardian Cloud Process Manager...")

# 1. Boot up the FastMCP Server asynchronously in the background
mcp_process = subprocess.Popen([
    sys.executable, "mcp_server.py"
])

# Yield execution time to let the SSE listener initialize fully
time.sleep(3)

# 2. Extract the dynamic ingress port provided by Google Cloud Run
cloud_run_port = os.getenv("PORT", "8501")

# 3. Boot the Streamlit visual interface
print(f"🌐 Directing frontend routing to interface port: {cloud_run_port}")
streamlit_process = subprocess.Popen([
    sys.executable, "-m", "streamlit", "run", "app.py",
    "--server.port", cloud_run_port,
    "--server.address", "0.0.0.0"
])

# Maintain persistence loops for both processes
try:
    mcp_process.wait()
    streamlit_process.wait()
except KeyboardInterrupt:
    print("🛑 Termination signal intercepted. Wiping active container instances...")
    mcp_process.terminate()
    streamlit_process.terminate()
