import subprocess
import json
import time

def inspect_foundit_card_dom():
    url = "https://www.foundit.in/srp/results?query=Python+Developer&experienceRanges=0~2&quickApplyJobs=true"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(5)
    
    js = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.trim() === 'Quick Apply' && !b.className.includes('Filter'));
        return btns.map(b => {
            let el = b;
            let parentTexts = [];
            for (let i = 0; i < 6; i++) {
                if (!el.parentElement) break;
                el = el.parentElement;
                parentTexts.push({ tag: el.tagName, class: el.className, textSlice: el.innerText.slice(0, 100) });
            }
            return {
                btnText: b.innerText,
                hierarchy: parentTexts
            };
        });
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("DOM CHECK:", res.stdout)
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    inspect_foundit_card_dom()
