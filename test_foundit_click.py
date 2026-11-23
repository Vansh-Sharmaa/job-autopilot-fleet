import subprocess
import json
import time

def test_foundit_click():
    url = "https://www.foundit.in/srp/results?query=Python+Developer&experienceRanges=0~2&quickApplyJobs=true"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(5)
    
    js = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.trim() === 'Quick Apply' && !b.className.includes('Filter'));
        if (btns.length === 0) return { status: 'no_buttons' };
        
        // Find parent card for this button
        let card = btns[0].closest('.card, [data-job-id], .srpResultCard') || btns[0].parentElement.parentElement;
        const comp = card?.querySelector('.companyName, .comp-name, .company')?.innerText?.trim() || '';
        const title = card?.querySelector('.jobTitle, .title, a')?.innerText?.trim() || '';
        
        btns[0].click();
        
        return {
            status: 'clicked',
            comp,
            title,
            remainingBtns: btns.length
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("CLICK RESULT:", res.stdout)
    
    time.sleep(3)
    
    # Check what changed on page
    check_js = """
    (() => {
        const toast = document.querySelector('.toast, .notification, .snackbar, .success')?.innerText;
        return {
            toast,
            snippet: document.body.innerText.slice(0, 300)
        };
    })()
    """
    res2 = subprocess.run(["browse", "eval", "--tab", str(tab_id), check_js], capture_output=True, text=True)
    print("AFTER CLICK:", res2.stdout)
    
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    test_foundit_click()
