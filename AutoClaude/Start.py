import webbrowser
import os
import sys
import subprocess
import time
import socket

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
    
    def get_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]

    port = get_free_port()
    print(f"Starting Backend.py on port {port}...")
    env = os.environ.copy()
    env["AUTOCLAUDE_PORT"] = str(port)
    backend_process = subprocess.Popen([sys.executable, backend_path], env=env)
    
    time.sleep(3)
    
    server_url = f"http://localhost:{port}"
    print(f"Opening {server_url} in default browser...")
    webbrowser.open(server_url)
    
    try:
        backend_process.wait()
    except KeyboardInterrupt:
        print("\nStopping backend...")
        backend_process.terminate()

if __name__ == "__main__":
    main()
