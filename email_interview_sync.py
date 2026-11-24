"""
JobPilot Email & Interview Intelligence Scanner
Connects to Gmail / IMAP, parses recruitment emails, categorizes interview stages,
extracts meeting links, and updates both the interview ledger and applications tracker.
Strictly zero em-dashes and zero en-dashes.
"""
import os
import sys
import json
import re
import imaplib
import email
from email.header import decode_header
from datetime import datetime

BASE_DIR = r"D:\opencode stuff\job-agents"
CONFIG_PATH = r"D:\opencode stuff\job-pilot-desktop\config.json"
INTERVIEWS_JSON = os.path.join(BASE_DIR, "interviews_tracker.json")
TRACKER_CSV = os.path.join(BASE_DIR, "job_applications_tracker.csv")

KEYWORDS_INTERVIEW = [
    "interview", "discussion", "video call", "google meet", "zoom meeting",
    "technical round", "hiring manager", "f2f", "walk-in", "schedule a time",
    "interview invitation", "screening call", "round 1", "round 2", "telephonic"
]

KEYWORDS_ASSESSMENT = [
    "assessment", "hackerrank", "hackerearth", "codility", "hirevue",
    "coding test", "coding challenge", "online test", "quiz link", "coderpad"
]

KEYWORDS_SHORTLIST = [
    "shortlist", "shortlisted", "next steps", "moving forward", "profile selected",
    "reviewed your profile", "impressed with your", "advance to next", "congratulations"
]

KEYWORDS_REJECTION = [
    "unfortunately", "not moving forward", "other candidates", "pursue other",
    "regret to inform", "unsuccessful", "wishing you success elsewhere", "position has been closed"
]

KEYWORDS_OFFER = [
    "job offer", "offer letter", "pleased to offer", "congratulations on your offer",
    "employment offer", "letter of intent", "compensation breakdown"
]

def clean_dashes(text):
    if not text:
        return ""
    return str(text).replace("\u2014", " - ").replace("\u2013", " - ")

def decode_mime_words(raw_header):
    if not raw_header:
        return ""
    decoded_fragments = decode_header(raw_header)
    output = []
    for frag, enc in decoded_fragments:
        if isinstance(frag, bytes):
            try:
                output.append(frag.decode(enc or "utf-8", errors="replace"))
            except Exception:
                output.append(frag.decode("latin1", errors="replace"))
        else:
            output.append(str(frag))
    return "".join(output)

def extract_meeting_link(text):
    if not text:
        return ""
    # Google Meet
    m = re.search(r'(https?://meet\.google\.com/[a-z0-9\-]+)', text, re.IGNORECASE)
    if m:
        return m.group(1)
    # Zoom
    m = re.search(r'(https?://[a-z0-9\.\-]*zoom\.us/[a-z0-9\-_\?=/]+)', text, re.IGNORECASE)
    if m:
        return m.group(1)
    # Microsoft Teams
    m = re.search(r'(https?://teams\.microsoft\.com/[a-z0-9\-_\?=/]+)', text, re.IGNORECASE)
    if m:
        return m.group(1)
    # Calendly / Cal.com
    m = re.search(r'(https?://calendly\.com/[a-z0-9\-_\?=/]+)', text, re.IGNORECASE)
    if m:
        return m.group(1)
    return ""

def extract_scheduled_time(text):
    if not text:
        return ""
    patterns = [
        r'(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)(?:\s*IST|\s*UTC|\s*EST)?)',
        r'((?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)[,\s]+\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+)',
        r'(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+(?:\s+\d{4})?\s+at\s+\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?)'
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return ""

def extract_company_name(sender, subject):
    clean_sender = clean_dashes(sender)
    clean_sub = clean_dashes(subject)

    # Patterns like 'Careers - NextAstra', 'Touch Consultants', 'Aditi Tech Application'
    if "-" in clean_sender:
        parts = clean_sender.split("-")
        candidate = parts[-1].strip()
        if len(candidate) > 2 and "Monster" not in candidate and "Apply" not in candidate:
            return candidate.replace(".", "")
    if "@" in clean_sender:
        domain = clean_sender.split("@")[-1].split(">")[0].strip()
        base = domain.split(".")[0].capitalize()
        if base not in ["Gmail", "Yahoo", "Outlook", "Indeed", "Foundit", "Linkedin", "Naukri"]:
            return base

    for p in [r'^([A-Z][a-zA-Z0-9\s]+)\s+(?:Application|Interview|Update)', r'at\s+([A-Z][a-zA-Z0-9\s]+)']:
        m = re.search(p, clean_sub)
        if m:
            found = m.group(1).strip()
            if len(found) > 2 and len(found) < 30:
                return found

    # Fallback to sender prefix
    first_part = re.sub(r'<.*?>', '', clean_sender).strip()
    return first_part if first_part else "Recruiter"

def extract_role_title(subject, snippet):
    combined = f"{subject} {snippet}".lower()
    common_roles = [
        "AI Engineer", "Machine Learning Engineer", "ML Engineer", "Data Scientist",
        "Python Developer", "Full Stack Developer", "Software Engineer", "Frontend Developer",
        "Backend Developer", "GenAI Developer", "Fresher", "Intern"
    ]
    for r in common_roles:
        if r.lower() in combined:
            return r
    return "AI / Software Engineer"

def classify_email(text):
    t = text.lower()
    for kw in KEYWORDS_OFFER:
        if kw in t:
            return "OFFER"
    for kw in KEYWORDS_REJECTION:
        if kw in t:
            return "REJECTED"
    for kw in KEYWORDS_INTERVIEW:
        if kw in t:
            return "INTERVIEW"
    for kw in KEYWORDS_SHORTLIST:
        if kw in t:
            return "SHORTLISTED"
    for kw in KEYWORDS_ASSESSMENT:
        if kw in t:
            return "ASSESSMENT"
    return "APPLIED"

def normalize_existing_records():
    if not os.path.exists(INTERVIEWS_JSON):
        return []
    try:
        with open(INTERVIEWS_JSON, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        return []

    normalized = []
    seen = set()

    for idx, item in enumerate(raw):
        sender = clean_dashes(item.get("sender", ""))
        subject = clean_dashes(item.get("subject", ""))
        snippet = clean_dashes(item.get("snippet", ""))
        existing_cat = item.get("category", "").upper()

        combined_text = f"{sender} {subject} {snippet}"
        category = classify_email(combined_text)
        if existing_cat in ["INTERVIEW", "SHORTLISTED", "ASSESSMENT", "REJECTED", "OFFER"]:
            category = existing_cat

        company = clean_dashes(item.get("company")) or extract_company_name(sender, subject)
        role = clean_dashes(item.get("role")) or extract_role_title(subject, snippet)
        meeting = item.get("meetingLink") or extract_meeting_link(snippet)
        sched = item.get("scheduledTime") or extract_scheduled_time(f"{subject} {snippet}")

        # Unique key to avoid duplicate noise
        key = f"{company.lower()}:{subject.lower()[:30]}"
        if key in seen:
            continue
        seen.add(key)

        date_val = clean_dashes(item.get("date", ""))
        if not date_val or date_val == "has attachment":
            date_val = "Nov 22, 2026"

        rec = {
            "id": f"mail_{idx + 1}",
            "company": company,
            "role": role,
            "category": category,
            "sender": sender,
            "subject": subject,
            "date": date_val,
            "scheduledTime": sched,
            "meetingLink": meeting,
            "snippet": snippet if snippet else subject,
            "account": item.get("account", "engagevansh@gmail.com"),
            "status": "Upcoming" if category == "INTERVIEW" else ("Action Required" if category in ["SHORTLISTED", "ASSESSMENT"] else "Processed")
        }
        normalized.append(rec)

    # Save normalized version back
    try:
        with open(INTERVIEWS_JSON, "w", encoding="utf-8") as f:
            json.dump(normalized, f, indent=2)
    except Exception as e:
        print(f"Warning: could not save normalized JSON: {e}")

    return normalized

def sync_imap_gmail(target_account=None):
    cfg = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            pass

    email_accounts = cfg.get("emailAccounts", [])
    if not email_accounts:
        old_cfg = cfg.get("emailConfig", {})
        if old_cfg and old_cfg.get("email"):
            email_accounts = [old_cfg]
        else:
            email_accounts = [
                {"id": "acc_engagevansh", "email": "engagevansh@gmail.com", "label": "Primary (Engage)", "appPassword": "", "imapHost": "imap.gmail.com", "imapPort": 993, "enabled": True},
                {"id": "acc_xalta26", "email": "xalta26@gmail.com", "label": "XALTA Dev", "appPassword": "", "imapHost": "imap.gmail.com", "imapPort": 993, "enabled": True},
                {"id": "acc_vishurou61", "email": "vishurou61@gmail.com", "label": "Vishu Applications", "appPassword": "", "imapHost": "imap.gmail.com", "imapPort": 993, "enabled": True},
                {"id": "acc_kalsharma908", "email": "kalsharma908@gmail.com", "label": "Kal Outreach", "appPassword": "", "imapHost": "imap.gmail.com", "imapPort": 993, "enabled": True}
            ]

    if target_account:
        email_accounts = [a for a in email_accounts if a.get("email") == target_account]

    existing = normalize_existing_records()
    seen_keys = {f"{x['company'].lower()}:{x['subject'].lower()[:30]}:{x.get('account', '').lower()}" for x in existing}
    all_new_records = []

    active_accounts = [a for a in email_accounts if a.get("enabled", True)]
    print(f"[EMAIL SYNC] Scanning {len(active_accounts)} active Gmail accounts...")

    for idx, acc in enumerate(active_accounts):
        user_email = acc.get("email", "").strip()
        app_pwd = acc.get("appPassword", "").strip()
        host = acc.get("imapHost", "imap.gmail.com").strip()
        port = int(acc.get("imapPort", 993))
        label = acc.get("label", user_email)

        if not user_email:
            continue

        if not app_pwd:
            print(f"[EMAIL SYNC] [{idx+1}/{len(active_accounts)}] Notice: {user_email} ({label}) has no App Password set yet. Keeping existing records.")
            continue

        print(f"[EMAIL SYNC] [{idx+1}/{len(active_accounts)}] Connecting to {host}:{port} for {user_email} via SSL...")
        try:
            mail = imaplib.IMAP4_SSL(host, port)
            mail.login(user_email, app_pwd)
            mail.select("INBOX", readonly=True)

            search_criteria = '(OR (OR (SUBJECT "interview") (SUBJECT "shortlist")) (OR (SUBJECT "assessment") (SUBJECT "application")))'
            status, data = mail.search(None, search_criteria)

            if status != "OK" or not data[0]:
                print(f"[EMAIL SYNC] {user_email}: No new matching recruitment emails found.")
                mail.logout()
                continue

            msg_ids = data[0].split()
            recent_ids = msg_ids[-30:] # Last 30 messages per account
            print(f"[EMAIL SYNC] {user_email}: Found {len(recent_ids)} matching messages. Parsing...")

            acc_new = []
            for mid in reversed(recent_ids):
                try:
                    res, msg_data = mail.fetch(mid, "(RFC822)")
                    if res != "OK":
                        continue
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    subject = decode_mime_words(msg.get("Subject", ""))
                    sender = decode_mime_words(msg.get("From", ""))
                    date_header = msg.get("Date", "")

                    body_text = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body_text += part.get_payload(decode=True).decode("utf-8", errors="replace")
                    else:
                        body_text = msg.get_payload(decode=True).decode("utf-8", errors="replace")

                    company = extract_company_name(sender, subject)
                    role = extract_role_title(subject, body_text)
                    cat = classify_email(f"{subject} {body_text}")
                    meeting = extract_meeting_link(body_text)
                    sched = extract_scheduled_time(body_text)

                    key = f"{company.lower()}:{subject.lower()[:30]}:{user_email.lower()}"
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)

                    clean_acc_prefix = user_email.split('@')[0]
                    rec = {
                        "id": f"mail_{clean_acc_prefix}_{int(datetime.now().timestamp())}_{len(all_new_records)}",
                        "company": clean_dashes(company),
                        "role": clean_dashes(role),
                        "category": cat,
                        "sender": clean_dashes(sender),
                        "subject": clean_dashes(subject),
                        "date": clean_dashes(date_header[:16] if date_header else datetime.now().strftime("%b %d, %Y")),
                        "scheduledTime": clean_dashes(sched),
                        "meetingLink": clean_dashes(meeting),
                        "snippet": clean_dashes(body_text[:200].replace("\n", " ")),
                        "account": user_email,
                        "status": "Upcoming" if cat == "INTERVIEW" else "Processed"
                    }
                    all_new_records.append(rec)
                    acc_new.append(rec)
                except Exception as e:
                    print(f"[EMAIL SYNC] Warning parsing message for {user_email}: {e}")

            mail.logout()
            print(f"[EMAIL SYNC] {user_email}: Added {len(acc_new)} fresh recruitment records.")

        except Exception as e:
            print(f"[EMAIL SYNC] IMAP connection failed for {user_email}: {e}")

    if all_new_records:
        merged = all_new_records + existing
        with open(INTERVIEWS_JSON, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2)
        print(f"[EMAIL SYNC] Total fresh records added across all accounts: {len(all_new_records)}.")
        return merged

    return existing

def parse_pasted_text(raw_text, account=None):
    text = clean_dashes(raw_text)
    cat = classify_email(text)
    sched = extract_scheduled_time(text)
    meeting = extract_meeting_link(text)
    role = extract_role_title(text, "")
    user_account = account or "engagevansh@gmail.com"
    
    # Try to extract company
    company = "Hiring Partner"
    for line in text.splitlines()[:5]:
        if "from:" in line.lower():
            company = extract_company_name(line, "")
            break
        m = re.search(r'(?:team at|careers at|interviews at|from)\s+([A-Za-z0-9\s]+)', line, re.IGNORECASE)
        if m:
            company = m.group(1).strip()
            break

    rec = {
        "id": f"mail_manual_{int(datetime.now().timestamp())}",
        "company": company,
        "role": role,
        "category": cat,
        "sender": "Manual Input / Paste",
        "subject": text.splitlines()[0][:80] if text.splitlines() else "Pasted Recruitment Email",
        "date": datetime.now().strftime("%b %d, %Y"),
        "scheduledTime": sched,
        "meetingLink": meeting,
        "snippet": text[:250].replace("\n", " "),
        "account": user_account,
        "status": "Upcoming" if cat == "INTERVIEW" else "Processed"
    }

    records = normalize_existing_records()
    records.insert(0, rec)
    with open(INTERVIEWS_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    return rec

if __name__ == "__main__":
    if "--sync" in sys.argv:
        target = None
        if "--account" in sys.argv:
            idx = sys.argv.index("--account")
            if idx + 1 < len(sys.argv):
                target = sys.argv[idx + 1]
        recs = sync_imap_gmail(target)
        print(f"Total synchronized records: {len(recs)}")
    elif "--parse-text" in sys.argv:
        idx = sys.argv.index("--parse-text")
        raw = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""
        acc = "engagevansh@gmail.com"
        if "--account" in sys.argv:
            aidx = sys.argv.index("--account")
            if aidx + 1 < len(sys.argv):
                acc = sys.argv[aidx + 1]
        res = parse_pasted_text(raw, acc)
        print(json.dumps(res))
    else:
        recs = normalize_existing_records()
        print(f"Normalized {len(recs)} interview records.")
