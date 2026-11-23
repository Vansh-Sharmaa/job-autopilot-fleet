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

def run_foundit_mass_engine():
    print("="*60, flush=True)
    print(" 🚀 STARTING FOUNDIT MASS QUICK-APPLY FLEET ENGINE", flush=True)
    applied_set = get_applied_set()
    print(f" Currently applied companies in tracker: {len(applied_set)}", flush=True)
    print("="*60, flush=True)
    
    queries = [
        "AI+Engineer",
        "Python+Developer",
        "Machine+Learning",
        "Data+Scientist",
        "Generative+AI",
        "Deep+Learning",
        "Associate+Software+Engineer",
        "Junior+Developer",
        "Software+Engineer",
        "Full+Stack+Developer"
    ]
    
    total_applied = 0
    
    for q in queries:
        print(f"\n[foundit] Searching query: {q}...", flush=True)
        url = f"https://www.foundit.in/srp/results?query={q}&experienceRanges=0~2&quickApplyJobs=true"
        nav_out = run_browse(["navigate", url])
        try:
            tab_id = json.loads(nav_out).get("tab")
        except:
            continue
            
        time.sleep(5)
        
        # Extract cards
        extract_js = """
        (() => {
            const wrappers = Array.from(document.querySelectorAll('.srpCardsWrapper'));
            return wrappers.map(w => {
                const lines = w.innerText.split('\\n').map(l => l.trim()).filter(Boolean);
                return {
                    title: lines[0] || '',
                    comp: lines[1] || '',
                    exp: lines[2] || '',
                    loc: lines[4] || 'India'
                };
            });
        })()
        """
        cards = eval_tab(tab_id, extract_js)
        if not isinstance(cards, list) or len(cards) == 0:
            print(" [foundit] No cards found, skipping.", flush=True)
            close_tab(tab_id)
            continue
            
        valid_candidates = []
        for c in cards:
            comp = c.get('comp', '').strip()
            title = c.get('title', '').strip()
            exp = c.get('exp', '').strip()
            loc = c.get('loc', 'India').strip()
            
            if not comp or comp == "Select All" or "confidential" in comp.lower():
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
                
            applied_set.add(norm_comp)
            valid_candidates.append(c)
            
        print(f" [foundit] {len(valid_candidates)} new valid candidates on this page.", flush=True)
        
        if valid_candidates:
            apply_js = """
            (() => {
                const selectAllLabel = Array.from(document.querySelectorAll('label, div, span')).find(el => el.innerText && el.innerText.trim() === 'Select All');
                if (selectAllLabel) selectAllLabel.click();
                
                const quickBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.trim() === 'Quick Apply' && !b.className.includes('Filter'));
                if (quickBtns.length > 0) {
                    quickBtns[0].click();
                    return 'clicked';
                }
                return 'no_btn';
            })()
            """
            res = eval_tab(tab_id, apply_js)
            time.sleep(3)
            
            if res == 'clicked':
                for vc in valid_candidates:
                    comp = vc['comp']
                    title = vc['title']
                    loc = vc.get('loc', 'India')
                    total_applied += 1
                    log_application(comp, title, loc, "foundit", url)
                    
        close_tab(tab_id)
        time.sleep(2)
        
    print(f"\n[foundit] Engine completed. Total new applied: {total_applied}", flush=True)

if __name__ == "__main__":
    run_foundit_mass_engine()
