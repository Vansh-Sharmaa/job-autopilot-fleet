import subprocess
import json
import time

def test_select_all():
    url = "https://www.foundit.in/srp/results?query=Python+Developer&experienceRanges=0~2&quickApplyJobs=true"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(5)
    
    js = """
    (() => {
        // Find select all checkbox or label
        const selectAllLabel = Array.from(document.querySelectorAll('label, div, span')).find(el => el.innerText && el.innerText.trim() === 'Select All');
        const selectAllInput = document.querySelector('input#quick-apply-check');
        
        let clicked = false;
        if (selectAllLabel) {
            selectAllLabel.click();
            clicked = 'label_clicked';
        } else if (selectAllInput) {
            selectAllInput.click();
            clicked = 'input_clicked';
        }
        
        // Find the mass quick apply button
        const quickBtns = Array.from(document.querySelectorAll('button')).map(b => ({ text: b.innerText.trim(), class: b.className }));
        
        return {
            clicked,
            quickBtns
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("SELECT ALL RESULT:", res.stdout)
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    test_select_all()
