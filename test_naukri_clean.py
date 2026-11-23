import subprocess
import json
import time
import csv
import os
import re

TRACKER_FILE = r"D:\opencode stuff\job-agents\job_applications_tracker.csv"

TIER_1_BANNED = {
    "google", "alphabet", "amazon", "microsoft", "meta", "facebook", 
    "apple", "uber", "swiggy", "razorpay", "zomato", "netflix"
}

SPAM_KEYWORDS = {
    "consultancy fee", "registration fee", "telecaller", "bpo", "voice process",
    "customer support", "sales executive", "telemarketing", "immigration",
    "placement fee", "training fee"
}

def get_applied_set():
    applied = set()
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 1:
                    applied.add(row[1].lower().strip())
    return applied

def is_valid_exp(exp_text):
    if not exp_text:
        return True
    exp_lower = exp_text.lower()
    if "fresher" in exp_lower:
        return True
    match = re.search(r"(\d+)\s*(?:-|to)\s*(\d+)", exp_lower)
    if match:
        min_exp = int(match.group(1))
        return min_exp <= 2
    single_match = re.search(r"(\d+)\+?\s*yr", exp_lower)
    if single_match:
        val = int(single_match.group(1))
        return val <= 2
    return True

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
        print(f" [!] Browse error: {e}", flush=True)
        return ""

def eval_tab(tab_id, js_code):
    out = run_browse(["eval", "--tab", str(tab_id), js_code])
    try:
        return json.loads(out)
    except:
        return out

def close_tab(tab_id):
    run_browse(["tabs", "--tab", str(tab_id), "close"])

def test_naukri_run():
    applied_set = get_applied_set()
    print(f"Currently applied companies in tracker: {len(applied_set)}", flush=True)
    
    url = "https://www.naukri.com/ai-engineer-jobs-in-india-0-to-2-years-experience"
    nav_out = run_browse(["navigate", url])
    tab_id = json.loads(nav_out).get("tab")
    time.sleep(4)
    
    js_extract = """
    (() => {
        const cards = Array.from(document.querySelectorAll('.srp-jobtuple-wrapper, .jobTuple'));
        return cards.map(c => {
            const titleEl = c.querySelector('.title, a[title]');
            const compEl = c.querySelector('.comp-name, .companyInfo a');
            const expEl = c.querySelector('.exp-wrap, .expwdth, .experience');
            return {
                title: titleEl ? titleEl.innerText.trim() : '',
                comp: compEl ? compEl.innerText.trim() : '',
                exp: expEl ? expEl.innerText.trim() : '',
                url: titleEl ? titleEl.href : ''
            };
        });
    })()
    """
    cards = eval_tab(tab_id, js_extract)
    close_tab(tab_id)
    
    if not isinstance(cards, list):
        print(f"Failed to get cards: {cards}", flush=True)
        return
        
    print(f"Extracted {len(cards)} cards from search page.", flush=True)
    
    applied_count = 0
    for c in cards:
        comp = c.get('comp', '').strip()
        title = c.get('title', '').strip()
        exp = c.get('exp', '').strip()
        job_url = c.get('url', '').strip()
        
        if not comp or not job_url:
            continue
        if comp.lower() in applied_set:
            print(f" [SKIP] Duplicate company: {comp}", flush=True)
            continue
        if any(b in comp.lower() for b in TIER_1_BANNED):
            print(f" [SKIP] Tier-1 company: {comp}", flush=True)
            continue
        if any(s in (title + " " + comp).lower() for s in SPAM_KEYWORDS):
            print(f" [SKIP] Spam/Consultancy: {comp} - {title}", flush=True)
            continue
        if not is_valid_exp(exp):
            print(f" [SKIP] Exp > 2 YOE ({exp}): {comp}", flush=True)
            continue
            
        print(f"\n ---> Checking candidate: {comp} | {title} (Exp: {exp})", flush=True)
        job_nav = run_browse(["navigate", job_url])
        try:
            job_tab = json.loads(job_nav).get("tab")
        except:
            continue
            
        time.sleep(3)
        
        # Check and click apply
        apply_js = """
        (() => {
            const text = document.body.innerText.toLowerCase();
            if (text.includes('already applied')) {
                return { status: 'already_applied' };
            }
            const btn = document.querySelector('#apply-button, button.apply-button-component');
            if (!btn) return { status: 'no_btn' };
            if (btn.innerText.toLowerCase().includes('company site')) {
                return { status: 'external' };
            }
            btn.click();
            return { status: 'clicked' };
        })()
        """
        res = eval_tab(job_tab, apply_js)
        print(f"      Apply result: {res}", flush=True)
        
        if isinstance(res, dict) and res.get('status') == 'clicked':
            time.sleep(2)
            # handle skip/modal if any
            modal_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button, a')).filter(b => {
                    const t = b.innerText.toLowerCase().trim();
                    return t === 'skip' || t === 'apply without updating' || t === 'continue' || t === 'apply anyway';
                });
                if (btns.length > 0) {
                    btns[0].click();
                    return 'modal_clicked';
                }
                return 'no_modal';
            })()
            """
            eval_tab(job_tab, modal_js)
            applied_count += 1
            applied_set.add(comp.lower())
            log_application(comp, title, "India", "Naukri", job_url)
            
        close_tab(job_tab)
        time.sleep(2)
        
    print(f"\nFinished test batch. Total new applied: {applied_count}", flush=True)

if __name__ == "__main__":
    test_naukri_run()
