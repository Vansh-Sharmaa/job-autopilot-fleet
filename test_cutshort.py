import subprocess
import json
import time

def inspect_cutshort():
    url = "https://cutshort.io/"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(5)
    
    js = """
    (() => {
        return {
            title: document.title,
            url: window.location.href,
            snippet: document.body.innerText.slice(0, 500)
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("CUTSHORT STATE:", res.stdout)
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    inspect_cutshort()
