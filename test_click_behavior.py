import subprocess
import json
import time

def inspect_click_behavior():
    url = "https://www.naukri.com/job-listings-generative-ai-engineer-infosys-pune-chennai-bengaluru-2-to-5-years-221026035352"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(4)
    
    # Click apply
    click_js = """
    (() => {
        const btn = document.querySelector('#apply-button, button.apply-button-component');
        if (btn) {
            btn.click();
            return { clicked: true, text: btn.innerText };
        }
        return { clicked: false };
    })()
    """
    res1 = subprocess.run(["browse", "eval", "--tab", str(tab_id), click_js], capture_output=True, text=True)
    print("CLICK RES:", res1.stdout)
    
    time.sleep(3)
    
    # Inspect what is on the page/modal now
    modal_js = """
    (() => {
        const modals = Array.from(document.querySelectorAll('.modal, .drawer, .chat-bot, [class*="chat"], [class*="modal"], [class*="apply-layer"], .apply-drawer'));
        const btns = Array.from(document.querySelectorAll('button, a')).map(b => b.innerText.trim()).filter(Boolean);
        const inputs = Array.from(document.querySelectorAll('input, textarea, select')).map(i => ({ type: i.type, name: i.name, placeholder: i.placeholder, value: i.value }));
        return {
            modalCount: modals.length,
            modalTexts: modals.map(m => m.innerText.slice(0, 200)),
            buttons: btns.slice(0, 15),
            inputs: inputs.slice(0, 10),
            bodySnippet: document.body.innerText.slice(0, 600)
        };
    })()
    """
    res2 = subprocess.run(["browse", "eval", "--tab", str(tab_id), modal_js], capture_output=True, text=True)
    print("MODAL STATE:", res2.stdout)
    
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    inspect_click_behavior()
