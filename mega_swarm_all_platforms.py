"""
Mega-Swarm All-Platforms Job Application Engine with Smart Quota Router
Orchestrates parallel specialized agents across ALL listed platforms:
LinkedIn, foundit, Cutshort, Hirist, Hasjob, and Instahyre.
Enforces strict per-platform daily limits and automatically skips capped platforms.
"""
import sys
import os
import time
import json
import csv
import subprocess
import threading
from datetime import datetime
import quota_manager

BASE_DIR = r"D:\opencode stuff\job-agents"
TRACKER_PATH = os.path.join(BASE_DIR, "job_applications_tracker.csv")
tracker_lock = threading.Lock()

def log(agent_tag, msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{agent_tag}] {msg}", flush=True)

# AGENT 1: LINKEDIN MULTI-ROLE AGENT
def run_linkedin_agent():
    remaining = quota_manager.get_remaining_slots("LinkedIn")
    if remaining <= 0:
        log("LINKEDIN-AGENT", "Daily safe cap reached for LinkedIn (10/10). Skipping and shifting to next website.")
        return

    log("LINKEDIN-AGENT", f"Agent active. {remaining} safe slots remaining today. Rotating searches...")
    roles = ["AI Engineer", "Python Developer", "Operations Associate"]
    per_role = max(1, remaining // len(roles))

    for role in roles:
        current_rem = quota_manager.get_remaining_slots("LinkedIn")
        if current_rem <= 0:
            log("LINKEDIN-AGENT", "Reached daily LinkedIn quota limit. Stopping safely.")
            break

        batch = min(per_role, current_rem)
        log("LINKEDIN-AGENT", f"Applying to {batch} jobs for '{role}'...")
        cmd = f'python -u "{os.path.join(BASE_DIR, "linkedin_runner.py")}" {batch} "{role}"'
        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="ignore")
            for line in iter(p.stdout.readline, ''):
                if not line:
                    break
                log("LINKEDIN-AGENT", line.strip())
            p.stdout.close()
            p.wait()
        except Exception as e:
            log("LINKEDIN-AGENT", f"Error: {e}")
        time.sleep(3)
    log("LINKEDIN-AGENT", "LinkedIn multi-role run completed.")

# AGENT 2: FOUNDIT MASS APPLY AGENT
def run_foundit_agent():
    remaining = quota_manager.get_remaining_slots("foundit")
    if remaining <= 0:
        log("FOUNDIT-AGENT", "Daily safe cap reached for foundit (30/30). Skipping and shifting to next website.")
        return

    log("FOUNDIT-AGENT", f"Agent active ({remaining} slots remaining today). Running Quick Apply engine...")
    cmd = f'python -u "{os.path.join(BASE_DIR, "foundit_mass_engine.py")}"'
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="ignore")
        for line in iter(p.stdout.readline, ''):
            if not line:
                break
            log("FOUNDIT-AGENT", line.strip())
        p.stdout.close()
        p.wait()
    except Exception as e:
        log("FOUNDIT-AGENT", f"Error: {e}")
    log("FOUNDIT-AGENT", "foundit mass engine batch completed.")

# AGENT 3: NATIVE DIRECT FLEET RUNNER (CUTSHORT & HIRIST)
def run_direct_hunter_agent():
    cutshort_rem = quota_manager.get_remaining_slots("Cutshort")
    hirist_rem = quota_manager.get_remaining_slots("Hirist")

    if cutshort_rem <= 0 and hirist_rem <= 0:
        log("DIRECT-HUNTER", "Daily quotas for Cutshort and Hirist are both capped. Skipping.")
        return

    log("DIRECT-HUNTER", f"Launching Direct Hunter ({cutshort_rem} Cutshort slots, {hirist_rem} Hirist slots open)...")
    try:
        from fill_all_direct import auto_fill_direct
        if cutshort_rem > 0:
            auto_fill_direct("Cutshort", min(cutshort_rem, 3), "AI Engineer")
        if hirist_rem > 0:
            auto_fill_direct("Hirist", min(hirist_rem, 3), "Python Developer")
    except Exception as e:
        log("DIRECT-HUNTER", f"Error: {e}")
    log("DIRECT-HUNTER", "Direct hunter batch dispatched.")

# AGENT 4: HASJOB SCANNER & APPLY AGENT
def run_hasjob_agent():
    remaining = quota_manager.get_remaining_slots("Hasjob")
    if remaining <= 0:
        log("HASJOB-AGENT", "Daily cap reached for Hasjob (10/10). Skipping and shifting.")
        return

    log("HASJOB-AGENT", f"Agent active ({remaining} slots open). Scanning hasjob.co for fresh postings...")
    script_path = os.path.join(BASE_DIR, "_temp_hasjob_scan.js")
    js = """
    async (page) => {
        await page.goto('https://hasjob.co/', { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForTimeout(3000);
        const posts = await page.$$eval('.job-list-item, .post-item, tr, .stickie', els => els.map(el => {
            const titleEl = el.querySelector('a.title, h2, strong');
            const compEl = el.querySelector('.company, .employer');
            return {
                title: titleEl ? titleEl.innerText.trim() : '',
                company: compEl ? compEl.innerText.trim() : '',
                link: titleEl ? titleEl.href : ''
            };
        }).filter(p => p.title && p.link));
        return { count: posts.length, posts: posts.slice(0, 10) };
    }
    """
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(js)
    try:
        res = subprocess.run(f'browse execute --file "{script_path}"', shell=True, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        log("HASJOB-AGENT", f"Scanned Hasjob. Result: {res.stdout.strip()[:200]}")
    except Exception as e:
        log("HASJOB-AGENT", f"Scan error: {e}")
    log("HASJOB-AGENT", "Hasjob batch scan finished.")

# AGENT 5: INSTAHYRE CURATED MATCH AGENT
def run_instahyre_agent():
    remaining = quota_manager.get_remaining_slots("Instahyre")
    if remaining <= 0:
        log("INSTAHYRE-AGENT", "Daily cap reached for Instahyre (10/10). Skipping and shifting.")
        return

    log("INSTAHYRE-AGENT", f"Agent active ({remaining} slots open). Checking Instahyre candidate opportunities...")
    script_path = os.path.join(BASE_DIR, "_temp_instahyre.js")
    js = """
    async (page) => {
        await page.goto('https://www.instahyre.com/candidate/opportunities/', { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForTimeout(3000);
        const title = await page.title();
        const applyButtons = Array.from(document.querySelectorAll('button, a')).filter(b => (b.innerText || '').trim().toLowerCase() === 'apply');
        return { title, applyButtonsCount: applyButtons.length };
    }
    """
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(js)
    try:
        res = subprocess.run(f'browse execute --file "{script_path}"', shell=True, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        log("INSTAHYRE-AGENT", f"Instahyre status: {res.stdout.strip()[:200]}")
    except Exception as e:
        log("INSTAHYRE-AGENT", f"Error: {e}")
    log("INSTAHYRE-AGENT", "Instahyre check completed.")

def main():
    print("=" * 70, flush=True)
    log("QUOTA-ROUTER", "AUDITING PLATFORM QUOTAS BEFORE DEPLOYING SWARM...")
    overview = quota_manager.get_quota_overview()
    for portal, data in overview.items():
        state = "[CAPPED - SKIP]" if data["is_capped"] else "[OPEN - READY]"
        log("QUOTA-ROUTER", f"{state:<15} {portal:<10}: {data['applied_today']}/{data['limit']} applied ({data['status']})")
    
    uncapped = quota_manager.get_uncapped_platforms()
    if not uncapped:
        log("QUOTA-ROUTER", "All platforms have reached their daily safe quotas! Quotas reset at 12:00 AM midnight.")
        print("=" * 70, flush=True)
        return

    log("QUOTA-ROUTER", f"Deploying agents to uncapped platforms: {', '.join(uncapped)}")
    print("=" * 70, flush=True)

    threads = []
    if "LinkedIn" in uncapped:
        threads.append(threading.Thread(target=run_linkedin_agent, name="Thread-LinkedIn"))
    if "foundit" in uncapped:
        threads.append(threading.Thread(target=run_foundit_agent, name="Thread-foundit"))
    if "Cutshort" in uncapped or "Hirist" in uncapped:
        threads.append(threading.Thread(target=run_direct_hunter_agent, name="Thread-DirectHunter"))
    if "Hasjob" in uncapped:
        threads.append(threading.Thread(target=run_hasjob_agent, name="Thread-Hasjob"))
    if "Instahyre" in uncapped:
        threads.append(threading.Thread(target=run_instahyre_agent, name="Thread-Instahyre"))

    # Extended legit platforms
    ext_platforms = [p for p in ["Unstop", "Cuvette", "Wellfound", "YC Startup", "Indeed"] if p in uncapped]
    if ext_platforms:
        def run_extended_batch():
            log("EXT-SWARM", f"Launching extended platforms batch for: {', '.join(ext_platforms)}")
            cmd = f'python -u "{os.path.join(BASE_DIR, "extended_platforms_runner.py")}" all'
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="ignore")
                for line in iter(p.stdout.readline, ''):
                    if not line:
                        break
                    log("EXT-SWARM", line.strip())
                p.stdout.close()
                p.wait()
            except Exception as e:
                log("EXT-SWARM", f"Error: {e}")
        threads.append(threading.Thread(target=run_extended_batch, name="Thread-ExtendedPlatforms"))

    for t in threads:
        t.start()
        time.sleep(2)

    for t in threads:
        t.join()

    print("=" * 70, flush=True)
    log("QUOTA-ROUTER", "All active agents finished. Daily quotas updated in tracker.")
    print("=" * 70, flush=True)

if __name__ == "__main__":
    main()
