import csv
import re
import os

TRACKER_PATH = r"D:\opencode stuff\job-agents\job_applications_tracker.csv"

# Banned keywords in title/company
NON_TECH_KEYWORDS = [
    "graphic designer", "helpdesk", "telecaller", "bpo", "voice process",
    "customer support", "sales executive", "telemarketing", "immigration",
    "placement fee", "training fee", "abroad job"
]

def clean_company_name(name):
    n = name.lower().strip()
    # Remove proprietor prefixes
    n = re.sub(r".*\(proprietor of\s*", "", n)
    n = re.sub(r"\)", "", n)
    # Remove corporate suffixes
    n = re.sub(r"\b(private limited|pvt ltd|pvt\. ltd\.|ltd\.|limited|technologies|solutions|llp|inc|corp)\b", "", n)
    n = re.sub(r"[^\w\s]", " ", n)
    return " ".join(n.split())

def clean_csv():
    raw_lines = []
    with open(TRACKER_PATH, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    # Fix merged lines where line doesn't end with newline before quotes
    fixed_text = text.replace('"Nexvia Technologies"', '\n2026-11-22,"Nexvia Technologies"')
    lines = fixed_text.splitlines()

    header = "date,company,role,location,portal,status,url"
    cleaned_rows = []
    seen_companies = set()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("date,company"):
            continue
        
        # Parse CSV line
        try:
            reader = csv.reader([line])
            row = next(reader)
        except Exception:
            continue

        if len(row) < 5:
            continue

        date = row[0].strip()
        company = row[1].strip()
        role = row[2].strip()
        location = row[3].strip() if len(row) > 3 else "India"
        portal = row[4].strip() if len(row) > 4 else "Online"
        status = row[5].strip() if len(row) > 5 else "Submitted"
        url = row[6].strip() if len(row) > 6 else ""

        # Check non-tech or spam
        combined = f"{company} {role}".lower()
        if any(bad in combined for bad in NON_TECH_KEYWORDS):
            print(f"[-] Dropping non-tech/spam: {company} | {role}")
            continue

        norm_comp = clean_company_name(company)
        if norm_comp in seen_companies or len(norm_comp) < 2:
            print(f"[-] Dropping duplicate: {company} | {role} (normalized: {norm_comp})")
            continue

        seen_companies.add(norm_comp)
        cleaned_rows.append([date, company, role, location, portal, status, url])

    # Write back clean CSV
    with open(TRACKER_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "company", "role", "location", "portal", "status", "url"])
        for r in cleaned_rows:
            writer.writerow(r)

    print(f"\n[+] Successfully cleaned CSV. Total unique, valid applications: {len(cleaned_rows)}")

if __name__ == "__main__":
    clean_csv()
