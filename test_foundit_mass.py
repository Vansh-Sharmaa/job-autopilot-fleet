import subprocess
import json
import time

def inspect_foundit_mass():
    url = "https://www.foundit.in/srp/results?query=Python+Developer&experienceRanges=0~2&quickApplyJobs=true"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(5)
    
    js = """
    (() => {
        const selectAllBox = document.querySelector('input[type="checkbox"]');
        const allCheckboxes = Array.from(document.querySelectorAll('input[type="checkbox"]')).map(cb => ({ id: cb.id, name: cb.name, checked: cb.checked, text: cb.parentElement?.innerText }));
        const btns = Array.from(document.querySelectorAll('button')).map(b => ({ text: b.innerText.trim(), class: b.className }));
        return {
            checkboxes: allCheckboxes.slice(0, 5),
            buttons: btns.filter(b => b.text.toLowerCase().includes('apply'))
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("FOUNDIT MASS INSPECT:", res.stdout)
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    inspect_foundit_mass()
