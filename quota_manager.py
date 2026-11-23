"""
Smart Platform Quota Manager & Cascade Router for Vansh Sharma
Enforces daily safety caps per platform, prevents account bans,
and automatically shifts execution to the next available website when a quota fills.
"""
import os
import csv
from datetime import datetime

BASE_DIR = r"D:\opencode stuff\job-agents"
TRACKER_PATH = os.path.join(BASE_DIR, "job_applications_tracker.csv")

# Strict Safe Daily Application Caps
PLATFORM_LIMITS = {
    "LinkedIn": 10,      # Strict anti-ban human pace
    "foundit": 30,       # Mass Quick-Apply tech cap
    "Cutshort": 10,      # High-match startup cap
    "Hirist": 10,        # Screening questionnaire cap
    "Instahyre": 10,     # Curated opportunities cap
    "Hasjob": 10,        # Developer board cap
    "Wellfound": 15,     # AngelList tech & AI startup cap
    "YC Startup": 15,    # Y Combinator Work at a Startup cap
    "Indeed": 25,        # High-volume corporate & tech cap
    "Glassdoor": 15,     # Company reviews & direct apply cap
    "Unstop": 20,        # Freshers, hackathons & hiring challenges cap
    "Cuvette": 20,       # Verified 0-2 YOE tech internships & roles cap
    "Otta": 15,          # Modern tech & engineering roles cap
    "Naukri": 50         # Platform candidate daily quota limit
}

def normalize_portal_name(name):
    if not name:
        return "Other"
    n = name.strip()
    nl = n.lower()
    if "linkedin" in nl:
        return "LinkedIn"
    if "foundit" in nl or "monster" in nl:
        return "foundit"
    if "cutshort" in nl:
        return "Cutshort"
    if "hirist" in nl:
        return "Hirist"
    if "instahyre" in nl:
        return "Instahyre"
    if "hasjob" in nl:
        return "Hasjob"
    if "wellfound" in nl or "angellist" in nl:
        return "Wellfound"
    if "ycombinator" in nl or "workatastartup" in nl or "yc" in nl:
        return "YC Startup"
    if "glassdoor" in nl:
        return "Glassdoor"
    if "indeed" in nl:
        return "Indeed"
    if "unstop" in nl or "dare2compete" in nl:
        return "Unstop"
    if "cuvette" in nl:
        return "Cuvette"
    if "otta" in nl or "welcome to the jungle" in nl:
        return "Otta"
    if "naukri" in nl:
        return "Naukri"
    return n

def get_today_counts():
    today = datetime.now().strftime("%Y-%m-%d")
    counts = {p: 0 for p in PLATFORM_LIMITS}
    
    if os.path.exists(TRACKER_PATH):
        try:
            with open(TRACKER_PATH, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    if r.get("date") == today:
                        portal = normalize_portal_name(r.get("portal", ""))
                        if portal in counts:
                            counts[portal] += 1
                        else:
                            counts[portal] = counts.get(portal, 0) + 1
        except Exception as e:
            print(f"[QUOTA-MANAGER] Error reading tracker: {e}")
    return counts

def can_apply(portal):
    norm = normalize_portal_name(portal)
    limit = PLATFORM_LIMITS.get(norm, 10)
    today_counts = get_today_counts()
    applied = today_counts.get(norm, 0)
    return applied < limit

def get_remaining_slots(portal):
    norm = normalize_portal_name(portal)
    limit = PLATFORM_LIMITS.get(norm, 10)
    today_counts = get_today_counts()
    applied = today_counts.get(norm, 0)
    return max(0, limit - applied)

def get_quota_overview():
    today_counts = get_today_counts()
    overview = {}
    for portal, limit in PLATFORM_LIMITS.items():
        applied = today_counts.get(portal, 0)
        remaining = max(0, limit - applied)
        is_capped = applied >= limit
        overview[portal] = {
            "limit": limit,
            "applied_today": applied,
            "remaining": remaining,
            "is_capped": is_capped,
            "status": "CAPPED (Resets 12:00 AM)" if is_capped else f"{remaining} slots open"
        }
    return overview

def get_uncapped_platforms():
    overview = get_quota_overview()
    return [p for p, data in overview.items() if not data["is_capped"]]

if __name__ == "__main__":
    print("=== PLATFORM DAILY QUOTA STATUS ===")
    status = get_quota_overview()
    for portal, data in status.items():
        state = "[CAPPED]" if data["is_capped"] else "[OPEN]"
        print(f" {state:<8} {portal:<12}: {data['applied_today']}/{data['limit']} applied ({data['status']})")
    print("\nNext uncapped platforms ready for Apply All:")
    print(" ->", ", ".join(get_uncapped_platforms()) or "None (All daily quotas exhausted!)")
