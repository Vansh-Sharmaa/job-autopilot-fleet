import subprocess
import json
import time
import csv

TRACKER_FILE = r"D:\opencode stuff\job-agents\job_applications_tracker.csv"

def check_jobs_status():
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)[1:]
    
    # filter naukri rows
    naukri_rows = [r for r in rows if len(r) > 6 and "naukri.com" in r[6]]
    print(f"Total Naukri rows in tracker: {len(naukri_rows)}")
    
    # Check 8 samples from different batches (early, middle, late)
    indices = [0, 5, 10, 20, 40, 70, 100, len(naukri_rows)-1]
    
    for idx in indices:
        if idx >= len(naukri_rows):
            continue
        row = naukri_rows[idx]
        comp, role, url = row[1], row[2], row[6]
        
        nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
        try:
            tab_id = json.loads(nav.stdout).get("tab")
        except:
            continue
        time.sleep(3)
        
        js = """
        (() => {
            const text = document.body.innerText;
            const hasAppliedBadge = Array.from(document.querySelectorAll('*')).some(el => el.innerText && el.innerText.trim() === 'Applied');
            const btn = document.querySelector('#apply-button, button.apply-button-component');
            return {
                hasAppliedBadge,
                btnText: btn ? btn.innerText.trim() : 'NO_BTN',
                snippetHasApplied: text.toLowerCase().includes('applied')
            };
        })()
        """
        res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
        print(f"[{idx}] {comp} | {role} -> {res.stdout.strip()}")
        subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)
        time.sleep(1)

if __name__ == "__main__":
    check_jobs_status()
