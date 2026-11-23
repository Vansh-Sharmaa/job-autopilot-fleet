import subprocess
import json
import time

def click_hyrezy():
    js = """
    (() => {
        const allEls = Array.from(document.querySelectorAll('*')).filter(el => el.innerText && el.innerText.includes('HYrEzy'));
        const deepest = allEls[allEls.length - 1];
        if (deepest) {
            // Find clickable card wrapper
            let target = deepest;
            for (let i = 0; i < 4; i++) {
                if (target.parentElement && (target.tagName === 'A' || target.parentElement.tagName === 'A' || target.role === 'button')) {
                    break;
                }
                target = target.parentElement;
            }
            target.click();
            return { clicked: true, tag: target.tagName, text: target.innerText.slice(0, 100) };
        }
        return { clicked: false };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437702", js], capture_output=True, text=True)
    print("CLICK RESULT:", res.stdout)
    
    time.sleep(3)
    
    # Check right pane
    pane_js = """
    (() => {
        const text = document.body.innerText;
        const easyApplyBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Easy Apply'));
        return {
            title: document.title,
            hasEasyApplyBtn: !!easyApplyBtn,
            easyApplyBtnText: easyApplyBtn ? easyApplyBtn.innerText.trim() : null
        };
    })()
    """
    res2 = subprocess.run(["browse", "eval", "--tab", "12437702", pane_js], capture_output=True, text=True)
    print("PANE AFTER CLICK:", res2.stdout)

if __name__ == "__main__":
    click_hyrezy()
