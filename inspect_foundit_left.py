import subprocess
import json
import time

def inspect_foundit_left_cards():
    url = "https://www.foundit.in/srp/results?query=Python+Developer&experienceRanges=0~2&quickApplyJobs=true"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(5)
    
    js = """
    (() => {
        const cards = Array.from(document.querySelectorAll('.srpResultCard'));
        return cards.map(c => {
            const lines = c.innerText.split('\\n').map(l => l.trim()).filter(Boolean);
            return {
                title: lines[0],
                comp: lines[1],
                lines: lines.slice(0, 6)
            };
        });
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("LEFT CARDS:", res.stdout)
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    inspect_foundit_left_cards()
