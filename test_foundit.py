import subprocess
import json
import time

def test_foundit():
    url = "https://www.foundit.in/srp/results?query=Python+Developer&experienceRanges=0~2&quickApplyJobs=true"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(5)
    
    js = """
    (() => {
        const cards = Array.from(document.querySelectorAll('.card, [data-job-id], .srpResultCard'));
        const quickBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.trim() === 'Quick Apply');
        return {
            title: document.title,
            cardsFound: cards.length,
            quickApplyBtnsCount: quickBtns.length,
            firstCardInfo: cards[0]?.innerText?.slice(0, 200)
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("FOUNDIT TEST:", res.stdout)
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    test_foundit()
