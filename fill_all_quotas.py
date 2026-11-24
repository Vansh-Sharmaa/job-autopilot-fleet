"""
Daily Quota Maximizer Engine for Vansh Sharma
Goal: Automatically loop through EVERY uncapped platform and apply until all daily limits are reached:
- LinkedIn: up to 10 (8 remaining)
- foundit: up to 30 (28 remaining)
- Cutshort: up to 10 (5 remaining)
- Hirist: up to 10 (9 remaining)
- Instahyre: up to 10 (10 remaining)
- Hasjob: up to 10 (10 remaining)
- Wellfound / YC / Indeed / Unstop / Cuvette: up to limits

Enforces 0-2 YOE, human pacing (15-20s pauses), 0 em-dashes, and RAM hygiene (max 2 tabs).
"""
import sys
import os
import time
import subprocess
import quota_manager

BASE_DIR = r"D:\opencode stuff\job-agents"

def log(tag, msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] [{tag}] {msg}", flush=True)

def fill_all_daily_quotas():
    log("MAXIMIZER", "==========================================================")
    log("MAXIMIZER", "STARTING DAILY QUOTA MAXIMIZER - GOAL: FILL ALL PLATFORMS")
    log("MAXIMIZER", "==========================================================")
    
    # Audit starting status
    overview = quota_manager.get_quota_overview()
    total_slots = sum(d["remaining"] for d in overview.values())
    log("MAXIMIZER", f"Total slots open across all uncapped platforms: {total_slots}")
    for p, d in overview.items():
        state = "[CAPPED]" if d["is_capped"] else f"[OPEN: {d['remaining']} slots]"
        log("MAXIMIZER", f" {p:<12}: {d['applied_today']}/{d['limit']} {state}")

    # STAGE 1: LINKEDIN EASY APPLY (Fill remaining slots)
    rem_linkedin = quota_manager.get_remaining_slots("LinkedIn")
    if rem_linkedin > 0:
        log("MAXIMIZER", f"Targeting LinkedIn: Filling {rem_linkedin} remaining slots across AI and Operations roles...")
        roles = ["AI Engineer", "Operations Associate"]
        for r in roles:
            cur_rem = quota_manager.get_remaining_slots("LinkedIn")
            if cur_rem <= 0:
                break
            batch = min(cur_rem, max(1, cur_rem // 2))
            log("MAXIMIZER", f"Running LinkedIn batch: {batch} jobs for '{r}'...")
            cmd = f'python -u "{os.path.join(BASE_DIR, "linkedin_runner.py")}" {batch} "{r}"'
            try:
                subprocess.run(cmd, shell=True, timeout=300)
            except Exception as e:
                log("MAXIMIZER", f"LinkedIn error: {e}")
            time.sleep(5)
    else:
        log("MAXIMIZER", "LinkedIn is already fully capped for today.")

    # STAGE 2: FOUNDIT MASS APPLY (Fill remaining slots)
    rem_foundit = quota_manager.get_remaining_slots("foundit")
    if rem_foundit > 0:
        log("MAXIMIZER", f"Targeting foundit: Filling {rem_foundit} remaining slots...")
        cmd = f'python -u "{os.path.join(BASE_DIR, "foundit_mass_engine.py")}"'
        try:
            subprocess.run(cmd, shell=True, timeout=360)
        except Exception as e:
            log("MAXIMIZER", f"foundit error: {e}")
        time.sleep(5)
    else:
        log("MAXIMIZER", "foundit is already fully capped for today.")

    # STAGE 3: CUTSHORT & HIRIST VIA NATIVE FLEET
    rem_cutshort = quota_manager.get_remaining_slots("Cutshort")
    rem_hirist = quota_manager.get_remaining_slots("Hirist")
    if rem_cutshort > 0 or rem_hirist > 0:
        log("MAXIMIZER", f"Targeting Cutshort ({rem_cutshort} slots) & Hirist ({rem_hirist} slots)...")
        try:
            from fill_all_direct import auto_fill_direct
            if rem_cutshort > 0:
                auto_fill_direct("Cutshort", rem_cutshort, "AI Engineer")
            if rem_hirist > 0:
                auto_fill_direct("Hirist", rem_hirist, "Python Developer")
        except Exception as e:
            log("MAXIMIZER", f"Fleet error: {e}")
        time.sleep(2)

    # STAGE 4: EXTENDED PLATFORMS (Unstop, Cuvette, Wellfound, YC, Indeed)
    ext_platforms = ["unstop", "cuvette", "wellfound", "yc", "indeed"]
    log("MAXIMIZER", "Targeting Extended Platforms (Unstop, Cuvette, Wellfound, YC Startup, Indeed)...")
    for plat in ext_platforms:
        cmd = f'python -u "{os.path.join(BASE_DIR, "extended_platforms_runner.py")}" {plat}'
        try:
            log("MAXIMIZER", f"Running extended runner for: {plat}")
            subprocess.run(cmd, shell=True, timeout=180)
        except Exception as e:
            log("MAXIMIZER", f"Error on {plat}: {e}")
        time.sleep(3)

    log("MAXIMIZER", "==========================================================")
    log("MAXIMIZER", "DAILY QUOTA MAXIMIZER CYCLE COMPLETED!")
    final_overview = quota_manager.get_quota_overview()
    for p, d in final_overview.items():
        state = "[CAPPED]" if d["is_capped"] else f"[REMAINING: {d['remaining']}]"
        log("MAXIMIZER", f" {p:<12}: {d['applied_today']}/{d['limit']} {state}")
    log("MAXIMIZER", "==========================================================")

if __name__ == "__main__":
    fill_all_daily_quotas()
