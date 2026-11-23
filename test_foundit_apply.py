import subprocess
import json
import time

def test_foundit_apply():
    url = "https://www.foundit.in/srp/results?query=Data+Scientist&experienceRanges=0~2&quickApplyJobs=true"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(5)
    
    js = """
    (() => {
        // Find select all
        const selectAll = document.querySelector('label[for="quick-apply-check"], #quick-apply-check');
        const cards = Array.from(document.querySelectorAll('.card, [data-job-id], .srpResultCard'));
        
        let extracted = [];
        cards.forEach(c => {
            const title = c.querySelector('.jobTitle, .title, a')?.innerText?.trim() || '';
            const comp = c.querySelector('.companyName, .comp-name, .company')?.innerText?.trim() || '';
            if (comp) extracted.push({ title, comp });
        });
        
        // Let's see the apply button for mass apply
        const quickApplyButtons = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.trim() === 'Quick Apply' && !b.className.includes('Filter'));
        
        return {
            extractedCount: extracted.length,
            extractedSample: extracted.slice(0, 5),
            quickApplyButtonsCount: quickApplyButtons.length,
            buttonTexts: quickApplyButtons.map(b => b.innerText.trim())
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("FOUNDIT APPLY TEST:", res.stdout)
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    test_foundit_apply()
