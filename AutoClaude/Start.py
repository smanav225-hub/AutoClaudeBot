import webbrowser
import os
import sys
import subprocess
import time
import socket

def kill_process_on_port(port):
    """Kills any process currently using the specified port on Windows."""
    try:
        # Find the PID using netstat
        result = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True).decode()
        for line in result.splitlines():
            if "LISTENING" in line:
                pid = line.strip().split()[-1]
                if pid != "0":
                    print(f"[CLEANUP] Found ghost process (PID {pid}) on port {port}. Killing it...")
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True)
                    time.sleep(1) # Give OS time to release the port
    except subprocess.CalledProcessError:
        # No process found on this port, which is fine
        pass

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_path = os.path.join(script_dir, "Backend.py")
    gui_path = os.path.join(script_dir, "GUI.html")
    
    if not os.path.exists(backend_path):
        print(f"Error: Could not find Backend.py at {backend_path}")
        return
    
    if not os.path.exists(gui_path):
        print(f"Error: Could not find GUI.html at {gui_path}")
        return
    
    port = 5000
    kill_process_on_port(port)
    
    print(f"Starting Backend.py on port {port}...")
    env = os.environ.copy()
    env["AUTOCLAUDE_PORT"] = str(port)
    
    # On Windows, we use CREATE_NEW_PROCESS_GROUP so we can kill the whole tree later
    backend_process = subprocess.Popen(
        [sys.executable, backend_path], 
        env=env,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    
    time.sleep(3)
    
    server_url = f"http://localhost:{port}"
    print(f"Opening {server_url} in default browser...")
    webbrowser.open(server_url)
    
    try:
        backend_process.wait()
    except KeyboardInterrupt:
        print("\nStopping backend...")
        # Use taskkill to ensure the entire process tree (all Discord bots) is killed
        subprocess.run(f"taskkill /F /T /PID {backend_process.pid}", shell=True, capture_output=True)

if __name__ == "__main__":
    main()
