import subprocess
import json
import time

def inspect_hirist():
    url = "https://www.hirist.tech/jobfeed?minexp=0&maxexp=2"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(5)
    
    js = """
    (() => {
        const text = document.body.innerText;
        const applyBtns = Array.from(document.querySelectorAll('button, a')).filter(b => b.innerText && b.innerText.trim().toLowerCase() === 'apply');
        const cards = Array.from(document.querySelectorAll('.job-card, .feed-card, [class*="job-card"], [class*="jobTuple"], [class*="feedCard"]'));
        return {
            title: document.title,
            applyBtnsCount: applyBtns.length,
            cardsCount: cards.length,
            snippet: text.slice(0, 600)
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("HIRIST STATE:", res.stdout)
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    inspect_hirist()
