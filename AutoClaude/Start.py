import webbrowser
import os
import sys
import subprocess
import time
import socket

def kill_process_on_port(port):
    """Kills any process currently using the specified port on Windows."""
    try:
        # Find the PID using netstat specifically for the listening port
        output = subprocess.check_output(f"netstat -ano | findstr LISTENING | findstr :{port}", shell=True).decode()
        pids = set()
        for line in output.splitlines():
            parts = line.strip().split()
            if parts:
                pids.add(parts[-1])
        
        for pid in pids:
            if pid != "0":
                print(f"[CLEANUP] Killing process tree for PID {pid} on port {port}...")
                # /F = force, /T = tree kill (kills child processes too)
                subprocess.run(f"taskkill /F /T /PID {pid}", shell=True, capture_output=True)
        
        if pids:
            time.sleep(2) # Give OS more time to release the port
    except subprocess.CalledProcessError:
        pass # No process found

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
