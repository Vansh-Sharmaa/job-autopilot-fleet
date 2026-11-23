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

TECH_TITLE_KEYWORDS = {
    "ai", "artificial intelligence", "machine learning", "ml", "python", 
    "data scientist", "data science", "deep learning", "genai", "generative ai", 
    "llm", "software engineer", "software developer", "full stack", "backend", 
    "frontend", "sde", "developer", "engineer", "trainee", "intern"
}

BANNED_TITLE_KEYWORDS = {
    "graphic", "designer", "helpdesk", "support", "sales", "marketing", 
    "telecaller", "bpo", "voice", "recruiter", "hr", "accountant", 
    "content writer", "immigration", "visa", "netherland", "germany", 
    "dubai", "australia", "abroad", "consultancy", "fee"
}

def clean_company_name(name):
    n = name.lower().strip()
    n = re.sub(r".*\(proprietor of\s*", "", n)
    n = re.sub(r"\)", "", n)
    n = re.sub(r"\b(private limited|pvt ltd|pvt\. ltd\.|ltd\.|limited|technologies|solutions|llp|inc|corp)\b", "", n)
    n = re.sub(r"[^\w\s]", " ", n)
    return " ".join(n.split())

def get_applied_set():
    applied = set()
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 1:
                    applied.add(clean_company_name(row[1]))
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
        print(f" [!] Browse error: {e}", flush=True)
        return ""

def eval_tab(tab_id, js_code):
    out = run_browse(["eval", "--tab", str(tab_id), js_code])
    try:
        return json.loads(out)
    except:
        return out

def close_tab(tab_id):
    if tab_id:
        run_browse(["tabs", "--tab", str(tab_id), "close"])

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

def is_valid_tech_role(title, comp):
    comb = f"{title} {comp}".lower()
    if any(b in comb for b in BANNED_TITLE_KEYWORDS):
        return False
    title_lower = title.lower()
    return any(t in title_lower for t in TECH_TITLE_KEYWORDS)

def run_naukri_fleet_phase2(max_target=65):
    print("\n" + "="*55, flush=True)
    print(" >>> STARTING NAUKRI 1-CLICK ENGINE - PHASE 2 (ANTIGRAVITY)", flush=True)
    print("="*55, flush=True)
    
    search_templates = [
        "ai-developer-jobs-0-to-2-years-experience",
        "deep-learning-engineer-jobs-0-to-2-years-experience",
        "machine-learning-jobs-in-bangalore-0-to-2-years-experience",
        "machine-learning-jobs-in-delhi-ncr-0-to-2-years-experience",
        "machine-learning-jobs-in-hyderabad-0-to-2-years-experience",
        "machine-learning-jobs-in-pune-0-to-2-years-experience",
        "python-developer-jobs-in-pune-0-to-2-years-experience",
        "python-developer-jobs-in-hyderabad-0-to-2-years-experience",
        "python-developer-jobs-in-mumbai-0-to-2-years-experience",
        "ai-engineer-jobs-in-hyderabad-0-to-2-years-experience",
        "ai-engineer-jobs-in-pune-0-to-2-years-experience",
        "ai-engineer-jobs-in-mumbai-0-to-2-years-experience",
        "junior-software-developer-jobs-0-to-1-years-experience",
        "backend-developer-jobs-0-to-2-years-experience",
        "full-stack-developer-jobs-0-to-2-years-experience",
        "artificial-intelligence-internship-jobs",
        "machine-learning-internship-jobs",
        "python-internship-jobs",
        "software-engineer-internship-jobs",
        "associate-software-engineer-jobs-0-to-2-years-experience",
        "graduate-engineer-trainee-jobs-0-to-1-years-experience"
    ]
    
    applied_count = 0
    applied_set = get_applied_set()
    
    for base_slug in search_templates:
        if applied_count >= max_target:
            break
            
        for page in range(1, 6):
            if applied_count >= max_target:
                break
                
            page_slug = base_slug if page == 1 else f"{base_slug}-{page}"
            url = f"https://www.naukri.com/{page_slug}?experience=0&experience=1&experience=2"
            
            print(f"\n[Naukri] Opening: {base_slug} (Page {page})...", flush=True)
            nav_out = run_browse(["navigate", url])
            try:
                tab_id = json.loads(nav_out).get("tab")
            except:
                continue
                
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
            
            if not isinstance(cards, list) or len(cards) == 0:
                print(" [Naukri] No cards on this page, moving to next search.", flush=True)
                break
                
            print(f" [Naukri] Extracted {len(cards)} cards.", flush=True)
            
            for c in cards:
                if applied_count >= max_target:
                    break
                    
                comp = c.get('comp', '').strip()
                title = c.get('title', '').strip()
                exp = c.get('exp', '').strip()
                job_url = c.get('url', '').strip()
                
                if not comp or not job_url:
                    continue
                    
                norm_comp = clean_company_name(comp)
                if norm_comp in applied_set:
                    continue
                if any(b in comp.lower() for b in TIER_1_BANNED):
                    continue
                if not is_valid_tech_role(title, comp):
                    continue
                if not is_valid_exp(exp):
                    continue
                    
                # Open single job
                job_nav = run_browse(["navigate", job_url])
                try:
                    job_tab = json.loads(job_nav).get("tab")
                except:
                    continue
                    
                time.sleep(3)
                
                # Check for 1-click apply button
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
                
                if isinstance(res, dict) and res.get('status') == 'clicked':
                    time.sleep(2)
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
                    applied_set.add(norm_comp)
                    log_application(comp, title, "India", "Naukri", job_url)
                    
                close_tab(job_tab)
                time.sleep(2)
                
            time.sleep(2)
            
    print(f"\n[Naukri] Completed fleet batch. Total new applied: {applied_count}", flush=True)
    return applied_count

if __name__ == "__main__":
    print("="*60, flush=True)
    print(" 🚀 STARTING ANTIGRAVITY HIGH-PRECISION FLEET - PHASE 2", flush=True)
    print(f" Current Unique Applications in Tracker: {len(get_applied_set())}", flush=True)
    print("="*60, flush=True)
    
    total = run_naukri_fleet_phase2(max_target=65)
    
    print("\n" + "="*60, flush=True)
    print(f" 🎯 FLEET BATCH FINISHED. New applied: {total}", flush=True)
    print(f" 🏆 Grand Total Unique: {len(get_applied_set())}", flush=True)
    print("="*60, flush=True)
