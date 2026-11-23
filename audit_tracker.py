import subprocess
import json
import time
import csv

TRACKER_FILE = r"D:\opencode stuff\job-agents\job_applications_tracker.csv"

def audit_tracker():
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)[1:]
    
    print(f"Total rows in tracker: {len(rows)}")
    
    # Audit first 30 Naukri jobs to see where quota kicked in
    confirmed_applied = []
    quota_or_not_applied = []
    
    naukri_rows = [r for r in rows if len(r) > 6 and "naukri.com" in r[6]]
    print(f"Testing first 25 Naukri rows...")
    
    for idx, r in enumerate(naukri_rows[:25]):
        comp, role, url = r[1], r[2], r[6]
        nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
        try:
            tab_id = json.loads(nav.stdout).get("tab")
        except:
            continue
        time.sleep(2.5)
        
        js = """
        (() => {
            const text = document.body.innerText;
            const hasApplied = Array.from(document.querySelectorAll('*')).some(el => el.innerText && el.innerText.trim() === 'Applied');
            const hasQuota = text.includes('daily quota has been expired');
            const btn = document.querySelector('#apply-button, button.apply-button-component');
            return {
                hasApplied,
                hasQuota,
                btnText: btn ? btn.innerText.trim() : 'NO_BTN'
            };
        })()
        """
        res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
        try:
            data = json.loads(res.stdout)
            if data.get('hasApplied'):
                confirmed_applied.append((comp, role))
                print(f" [+] CONFIRMED APPLIED: {comp} | {role}")
            else:
                quota_or_not_applied.append((comp, role, data.get('btnText')))
                print(f" [-] NOT APPLIED: {comp} | {role} (btn: {data.get('btnText')})")
        except:
            pass
            
        subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)
        time.sleep(1)

    print(f"\n--- AUDIT SUMMARY ---")
    print(f"Confirmed Applied: {len(confirmed_applied)}")
    print(f"Not Applied: {len(quota_or_not_applied)}")

if __name__ == "__main__":
    audit_tracker()
