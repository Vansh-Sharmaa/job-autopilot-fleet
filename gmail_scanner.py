"""
Multi-Account Gmail Inbound Assessment & Shortlist Scanner
Scans all 4 active signed-in Gmail accounts in Brave:
1. engagevansh@gmail.com (Slot u/0)
2. xalta26@gmail.com (Slot u/1)
3. vishurou61@gmail.com (Slot u/2)
4. kalsharma908@gmail.com (Slot u/3)

Extracts:
- Category: SHORTLISTED, ASSESSMENT, INTERVIEW, UPDATE, REJECTED
- Sender, Subject, Snippet, Date, Link
- Strict RAM Hygiene: Navigates one tab at a time and closes it immediately.
"""
import subprocess
import json
import re
import os
import time

BASE_DIR = r"D:\opencode stuff\job-agents"
TRACKER_PATH = os.path.join(BASE_DIR, "interviews_tracker.json")

ACCOUNTS = [
    {"slot": 0, "email": "engagevansh@gmail.com"},
    {"slot": 1, "email": "xalta26@gmail.com"},
    {"slot": 2, "email": "vishurou61@gmail.com"},
    {"slot": 3, "email": "kalsharma908@gmail.com"}
]

KEYWORDS_INTERVIEW = ["interview", "discussion", "chat", "meeting", "call with", "round", "technical discussion", "f2f", "walk-in"]
KEYWORDS_TEST = ["assessment", "hackerearth", "hackerrank", "codility", "hirevue", "test link", "test invitation", "online test", "coding challenge", "quiz", "test scheduled", "coderpad"]
KEYWORDS_SHORTLIST = ["shortlist", "shortlisted", "reviewed your application", "next round", "next steps", "moving forward", "profile selected", "status update"]
KEYWORDS_REJECTION = ["unfortunately", "not moving forward", "other candidates", "pursue other", "regret", "unsuccessful"]

def classify_text(text):
    t = text.lower()
    for kw in KEYWORDS_REJECTION:
        if kw in t:
            return "REJECTED"
    for kw in KEYWORDS_SHORTLIST:
        if kw in t:
            return "SHORTLISTED"
    for kw in KEYWORDS_TEST:
        if kw in t:
            return "ASSESSMENT"
    for kw in KEYWORDS_INTERVIEW:
        if kw in t:
            return "INTERVIEW"
    return "UPDATE"

def parse_snapshot_lines(output, account_email, tab_url):
    results = []
    pattern = re.compile(r'checkbox "(?:unread,\s*)?([^",]+),\s*([^",]+),\s*([^",]+),\s*(.*)"\s*\[ref=([^\]]+)\]')
    alt_pattern = re.compile(r'checkbox "(?:unread,\s*)?([^",]+),\s*([^"]+)"\s*\[ref=([^\]]+)\]')

    for line in output.splitlines():
        line = line.strip()
        if not line.startswith("- checkbox"):
            continue
        if 'checkbox "checkbox"' in line:
            continue

        m = pattern.search(line)
        if m:
            sender = m.group(1).strip()
            subject = m.group(2).strip()
            date = m.group(3).strip()
            snippet = m.group(4).strip()
            cat = classify_text(f"{sender} {subject} {snippet}")
            results.append({
                "account": account_email,
                "sender": sender,
                "subject": subject,
                "date": date,
                "snippet": snippet,
                "category": cat,
                "link": tab_url
            })
            continue

        m2 = alt_pattern.search(line)
        if m2:
            sender = m2.group(1).strip()
            rest = m2.group(2).strip()
            cat = classify_text(f"{sender} {rest}")
            results.append({
                "account": account_email,
                "sender": sender,
                "subject": rest,
                "date": "",
                "snippet": rest,
                "category": cat,
                "link": tab_url
            })

    return results

def scan_account(acc):
    slot = acc["slot"]
    email = acc["email"]
    search_url = f"https://mail.google.com/mail/u/{slot}/#search/assessment+OR+interview+OR+test+OR+shortlisted"
    print(f"\n[SCANNER] Opening slot u/{slot} ({email})...", flush=True)

    tab_id = None
    try:
        nav = subprocess.run(["browse", "navigate", search_url], capture_output=True, text=True, timeout=35)
        nav_data = json.loads(nav.stdout)
        tab_id = nav_data.get("tab")
        print(f"[SCANNER] Loaded slot u/{slot} in tab {tab_id}. Waiting for emails to render...", flush=True)
        time.sleep(3)

        snap = subprocess.run(["browse", "snapshot", "--tab", str(tab_id)], capture_output=True, text=True, encoding="utf-8", errors="ignore")
        items = parse_snapshot_lines(snap.stdout, email, search_url)
        print(f"[SCANNER] Successfully parsed {len(items)} messages from {email}", flush=True)
        return items
    except Exception as e:
        print(f"[SCANNER] Error scanning {email}: {e}", flush=True)
        return []
    finally:
        if tab_id:
            try:
                subprocess.run(["browse", "tabs", "close", "--tab", str(tab_id)], capture_output=True)
                print(f"[SCANNER] Closed temporary tab {tab_id} for memory hygiene.", flush=True)
            except Exception:
                pass

def run_all_inboxes():
    print("=" * 65, flush=True)
    print("STARTING MULTI-ACCOUNT GMAIL SCANNER FOR ALL 4 INBOXES", flush=True)
    print("=" * 65, flush=True)

    all_results = []
    for acc in ACCOUNTS:
        found = scan_account(acc)
        all_results.extend(found)
        time.sleep(2)

    # Load existing tracker entries
    existing = []
    if os.path.exists(TRACKER_PATH):
        try:
            with open(TRACKER_PATH, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = []

    keys = {f"{x.get('account')}:{x.get('sender')}:{x.get('subject')}" for x in existing}
    new_count = 0
    for item in all_results:
        key = f"{item.get('account')}:{item.get('sender')}:{item.get('subject')}"
        if key not in keys:
            existing.append(item)
            keys.add(key)
            new_count += 1

    with open(TRACKER_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)

    shortlists = [x for x in existing if x.get("category") == "SHORTLISTED"]
    tests = [x for x in existing if x.get("category") == "ASSESSMENT"]
    interviews = [x for x in existing if x.get("category") == "INTERVIEW"]

    print("\n" + "=" * 65, flush=True)
    print(f"MULTI-INBOX SCAN COMPLETE!", flush=True)
    print(f"Total Emails Indexed: {len(existing)} (New: {new_count})", flush=True)
    print(f" - Shortlisted: {len(shortlists)}", flush=True)
    print(f" - Assessments / Test Links: {len(tests)}", flush=True)
    print(f" - Interview Invites / Chats: {len(interviews)}", flush=True)
    print("=" * 65, flush=True)

    return {
        "total": len(existing),
        "shortlisted": len(shortlists),
        "assessments": len(tests),
        "interviews": len(interviews),
        "items": existing
    }

if __name__ == "__main__":
    run_all_inboxes()
