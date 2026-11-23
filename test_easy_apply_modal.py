import subprocess
import json
import time

def test_easy_apply_click():
    js = """
    (() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Easy Apply'));
        if (btn) {
            btn.click();
            return { clicked: true, text: btn.innerText.trim() };
        }
        return { clicked: false };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437702", js], capture_output=True, text=True)
    print("CLICK EASY APPLY:", res.stdout)
    
    time.sleep(3)
    
    modal_js = """
    (() => {
        const dialog = document.querySelector('[role="dialog"], .jobs-easy-apply-modal, .artdeco-modal');
        const btns = dialog ? Array.from(dialog.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean) : [];
        const inputs = dialog ? Array.from(dialog.querySelectorAll('input, select, textarea')).map(i => ({
            name: i.name,
            type: i.type,
            placeholder: i.placeholder,
            value: i.value
        })) : [];
        return {
            hasModal: !!dialog,
            modalSnippet: dialog ? dialog.innerText.slice(0, 500) : null,
            buttons: btns,
            inputs: inputs
        };
    })()
    """
    res2 = subprocess.run(["browse", "eval", "--tab", "12437702", modal_js], capture_output=True, text=True)
    print("MODAL STATE:", res2.stdout)

if __name__ == "__main__":
    test_easy_apply_click()
