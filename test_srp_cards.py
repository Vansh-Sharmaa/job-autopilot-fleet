import subprocess
import json
import time

def test_srp_cards():
    url = "https://www.foundit.in/srp/results?query=Python+Developer&experienceRanges=0~2&quickApplyJobs=true"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(5)
    
    js = """
    (() => {
        const wrappers = Array.from(document.querySelectorAll('.srpCardsWrapper'));
        return wrappers.map(w => {
            const btn = w.querySelector('button');
            const lines = w.innerText.split('\\n').map(l => l.trim()).filter(Boolean);
            return {
                title: lines[0],
                comp: lines[1],
                exp: lines[2],
                btnText: btn ? btn.innerText.trim() : null
            };
        });
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("WRAPPERS:", res.stdout)
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    test_srp_cards()
