import subprocess
import json
import time

def check_single_job():
    url = "https://www.naukri.com/job-listings-software-engineer-qualcomm-bengaluru-0-to-1-years-261026005898"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(4)
    
    js = """
    (() => {
        const btn = document.querySelector('#apply-button, button.apply-button-component');
        const text = document.body.innerText;
        return {
            title: document.title,
            btnText: btn ? btn.innerText.trim() : 'NO_BTN',
            alreadyApplied: text.toLowerCase().includes('already applied') || text.toLowerCase().includes('you applied'),
            snippet: text.slice(0, 500)
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("QUALCOMM CHECK:", res.stdout)
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    check_single_job()
