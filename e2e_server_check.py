import subprocess
import time
import urllib.request
import sys

def test_live_server():
    print("Starting Streamlit server on localhost:8501...")
    cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port=8501",
        "--server.headless=true",
        "--browser.serverAddress=localhost"
    ]
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        # Wait up to 15 seconds for the server to spin up and respond to health check
        started = False
        health_url = "http://localhost:8501/_stcore/health"
        
        for attempt in range(15):
            time.sleep(1)
            try:
                with urllib.request.urlopen(health_url, timeout=2) as resp:
                    if resp.status == 200:
                        content = resp.read().decode('utf-8')
                        print(f"  [PASS] Streamlit Health Endpoint 200 OK (Response: '{content.strip()}')")
                        started = True
                        break
            except Exception:
                continue
                
        if not started:
            raise RuntimeError("Streamlit server failed to start within 15 seconds.")

        # Test Main Webpage Response
        main_url = "http://localhost:8501/"
        with urllib.request.urlopen(main_url, timeout=5) as resp:
            html = resp.read().decode('utf-8')
            assert resp.status == 200
            assert "<!doctype html>" in html.lower() or "streamlit" in html.lower()
            print("  [PASS] Streamlit Main Webpage HTTP 200 OK rendered successfully.")

        print("  [PASS] All Live Localhost Server Tests Completed Successfully!")
    finally:
        print("Terminating test server...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        print("Server terminated cleanly.")

if __name__ == "__main__":
    test_live_server()
