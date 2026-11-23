import subprocess
import json
import time

def test_foundit_cards_click():
    url = "https://www.foundit.in/srp/results?query=Python+Developer&experienceRanges=0~2&quickApplyJobs=true"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(5)
    
    js = """
    (() => {
        // Look for all job cards in the left pane
        const cards = Array.from(document.querySelectorAll('.srpResultCard, [id*="card-"]'));
        const cardTitles = cards.map(c => {
            const lines = c.innerText.split('\\n').map(l => l.trim()).filter(Boolean);
            return lines.slice(0, 3).join(' | ');
        });
        return {
            totalCards: cards.length,
            cardTitles: cardTitles.slice(0, 10)
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("FOUNDIT CARDS:", res.stdout)
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    test_foundit_cards_click()
