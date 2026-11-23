import subprocess
import json
import time
import csv
import os

TRACKER_FILE = r"D:\opencode stuff\job-agents\job_applications_tracker.csv"

def get_applied_set():
    applied = set()
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 1:
                    applied.add(row[1].lower().strip())
    return applied

def log_application(company, role, location, portal, url):
    with open(TRACKER_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d"), company, role, location, portal, "Submitted", url])
    print(f" [+] LOGGED: {company} | {role} ({portal})", flush=True)

def run_browse(cmd_args):
    try:
        res = subprocess.run(["browse"] + cmd_args, capture_output=True, text=True, timeout=60)
        return res.stdout.strip()
    except Exception as e:
        print(f"Browse error: {e}", flush=True)
        return ""

def eval_tab(tab_id, js_code):
    out = run_browse(["eval", "--tab", str(tab_id), js_code])
    try:
        return json.loads(out)
    except:
        return out

def close_tab(tab_id):
    run_browse(["tabs", "--tab", str(tab_id), "close"])

def test_foundit_batch():
    applied_set = get_applied_set()
    url = "https://www.foundit.in/srp/results?query=AI+Engineer&experienceRanges=0~2&quickApplyJobs=true"
    nav = run_browse(["navigate", url])
    tab_id = json.loads(nav).get("tab")
    time.sleep(5)
    
    # Extract visible cards with Quick Apply
    extract_js = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.trim() === 'Quick Apply' && !b.className.includes('Filter'));
        return btns.map((b, idx) => {
            let container = b.closest('.jdContent, .srpJdContainer, .srpResultCard') || b.parentElement.parentElement;
            let text = container ? container.innerText : '';
            let lines = text.split('\\n').map(l => l.trim()).filter(Boolean);
            return {
                idx,
                title: lines[0] || 'AI Engineer',
                comp: lines[1] || 'Foundit Employer',
                btnText: b.innerText.trim()
            };
        });
    })()
    """
    items = eval_tab(tab_id, extract_js)
    print(f"Found {len(items)} quick apply buttons on foundit.", flush=True)
    print(f"Items: {items}", flush=True)
    
    close_tab(tab_id)

if __name__ == "__main__":
    test_foundit_batch()
