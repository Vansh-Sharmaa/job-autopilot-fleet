import subprocess
import json
import time

def test_foundit_single():
    url = "https://www.foundit.in/srp/results?query=Machine+Learning&experienceRanges=0~2&quickApplyJobs=true"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(5)
    
    js = """
    (() => {
        const cards = Array.from(document.querySelectorAll('.card, [data-job-id], .srpResultCard'));
        const firstCard = cards[0];
        if (!firstCard) return { status: 'no_cards' };
        
        const title = firstCard.querySelector('.jobTitle, .title, a')?.innerText?.trim() || '';
        const comp = firstCard.querySelector('.companyName, .comp-name, .company')?.innerText?.trim() || '';
        const btn = Array.from(firstCard.querySelectorAll('button')).find(b => b.innerText.trim() === 'Quick Apply');
        
        return {
            title,
            comp,
            hasBtn: !!btn,
            btnClass: btn ? btn.className : null
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("CARD CHECK:", res.stdout)
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    test_foundit_single()
