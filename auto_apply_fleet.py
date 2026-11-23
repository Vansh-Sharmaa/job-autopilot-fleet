import subprocess
import json
import time
import csv
import os
import re

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
    print(f" [+] LOGGED: {company} | {role} ({portal})")

def run_browse(cmd_args):
    try:
        res = subprocess.run(["browse"] + cmd_args, capture_output=True, text=True, timeout=60)
        return res.stdout.strip()
    except Exception as e:
        print(f" [!] Browse error: {e}")
        return ""

def eval_tab(tab_id, js_code):
    out = run_browse(["eval", "--tab", str(tab_id), js_code])
    try:
        return json.loads(out)
    except:
        return out

def close_tab(tab_id):
    run_browse(["tabs", "--tab", str(tab_id), "close"])

def run_foundit_batch(max_jobs=35):
    print("\n" + "="*50)
    print(" >>> STARTING FOUNDIT BATCH")
    print("="*50)
    
    queries = [
        "AI+Engineer",
        "Python+Developer",
        "Machine+Learning",
        "Generative+AI"
    ]
    
    applied_count = 0
    applied_set = get_applied_set()
    
    for q in queries:
        if applied_count >= max_jobs:
            break
            
        print(f"\nSearching foundit: {q} (0-2 YOE)...")
        url = f"https://www.foundit.in/srp/results?query={q}&experienceRanges=0~2&quickApplyJobs=true"
        
        # Navigate
        nav_out = run_browse(["navigate", url])
        try:
            nav_data = json.loads(nav_out)
            tab_id = nav_data.get("tab")
        except:
            print("Failed to open foundit tab.")
            continue
            
        time.sleep(4)
        
        # Extract cards
        js_extract = """
        (() => {
            const cards = Array.from(document.querySelectorAll('.card, [data-job-id], .srpResultCard, .jobTuple'));
            return cards.map(c => {
                const title = c.querySelector('.jobTitle, .title, a')?.innerText?.trim() || '';
                const comp = c.querySelector('.companyName, .comp-name, .company')?.innerText?.trim() || '';
                const loc = c.querySelector('.location, .loc')?.innerText?.trim() || 'India';
                const hasQuick = !!Array.from(c.querySelectorAll('button')).find(b => b.innerText.trim() === 'Quick Apply');
                return { title, comp, loc, hasQuick };
            });
        })()
        """
        cards = eval_tab(tab_id, js_extract)
        if isinstance(cards, list):
            print(f"Found {len(cards)} job cards on foundit.")
            for idx, c in enumerate(cards):
                if applied_count >= max_jobs:
                    break
                comp = c.get('comp', '').strip()
                title = c.get('title', '').strip()
                loc = c.get('loc', 'India').strip()
                
                if not comp or comp.lower() in applied_set:
                    continue
                if not c.get('hasQuick', False):
                    continue
                    
                # Click quick apply on this card
                click_js = f"""
                (() => {{
                    const btns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.trim() === 'Quick Apply' && !b.className.includes('Filter'));
                    if (btns.length > 0) {{
                        btns[0].click();
                        return 'clicked';
                    }}
                    return 'none';
                }})()
                """
                res = eval_tab(tab_id, click_js)
                if res == 'clicked':
                    applied_count += 1
                    applied_set.add(comp.lower())
                    log_application(comp, title, loc, "foundit", url)
                    time.sleep(4)
        
        close_tab(tab_id)
        time.sleep(2)
        
    print(f"Foundit batch completed. Applied: {applied_count}")
    return applied_count

def run_naukri_batch(max_jobs=40):
    print("\n" + "="*50)
    print(" >>> STARTING NAUKRI BATCH")
    print("="*50)
    
    naukri_urls = [
        "https://www.naukri.com/ai-engineer-jobs-in-bangalore-0-to-2-years-experience?ctcFilter=3to6",
        "https://www.naukri.com/generative-ai-engineer-jobs-0-to-2-years-experience",
        "https://www.naukri.com/python-developer-jobs-in-bangalore-0-to-2-years-experience"
    ]
    
    applied_count = 0
    applied_set = get_applied_set()
    
    for n_url in naukri_urls:
        if applied_count >= max_jobs:
            break
            
        print(f"\nOpening Naukri search: {n_url.split('/')[-1]}...")
        nav_out = run_browse(["navigate", n_url])
        try:
            tab_id = json.loads(nav_out).get("tab")
        except:
            continue
            
        time.sleep(4)
        
        # Extract direct apply listings
        js_extract = """
        (() => {
            const cards = Array.from(document.querySelectorAll('.srp-jobtuple-wrapper, .jobTuple'));
            return cards.slice(0, 15).map(c => {
                const titleEl = c.querySelector('.title, a[title]');
                const compEl = c.querySelector('.comp-name, .companyInfo a');
                const expEl = c.querySelector('.exp-wrap, .experience');
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
        
        if isinstance(cards, list):
            print(f"Found {len(cards)} listings on Naukri.")
            for c in cards:
                if applied_count >= max_jobs:
                    break
                comp = c.get('comp', '').strip()
                title = c.get('title', '').strip()
                job_url = c.get('url', '').strip()
                
                if not comp or comp.lower() in applied_set:
                    continue
                if not job_url:
                    continue
                    
                # Open single job page
                job_nav = run_browse(["navigate", job_url])
                try:
                    job_tab = json.loads(job_nav).get("tab")
                except:
                    continue
                    
                time.sleep(3)
                
                # Check for Apply button (not external)
                apply_js = """
                (() => {
                    const btn = document.querySelector('#apply-button, button.apply-button-component');
                    if (btn && !btn.innerText.toLowerCase().includes('company site')) {
                        btn.click();
                        return 'applied';
                    }
                    return 'skip';
                })()
                """
                res = eval_tab(job_tab, apply_js)
                if res == 'applied':
                    applied_count += 1
                    applied_set.add(comp.lower())
                    log_application(comp, title, "Bengaluru / India", "Naukri", job_url)
                    time.sleep(3)
                    
                close_tab(job_tab)
                time.sleep(2)
                
    print(f"Naukri batch completed. Applied: {applied_count}")
    return applied_count

if __name__ == "__main__":
    print("==================================================")
    print(" 🚀 STARTING DISTRIBUTED HIGH-VOLUME FLEET")
    print("==================================================")
    total = 0
    total += run_foundit_batch(max_jobs=35)
    total += run_naukri_batch(max_jobs=40)
    print("\n" + "="*50)
    print(f" 🎯 TOTAL NEW APPLICATIONS SUBMITTED: {total}")
    print("==================================================")
