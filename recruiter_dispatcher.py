"""
Recruiter Cold-Email & LinkedIn InMail Dispatcher for Vansh Sharma
Bypasses traditional ATS filters by sending personalized, high-intent messages directly to recruiters and engineering hiring managers.
Strictly 0 em-dashes and human-written phrasing citing real projects.
"""
import os
import sys
import json
import csv
from datetime import datetime

BASE_DIR = r"D:\opencode stuff\job-agents"
OUTREACH_TRACKER = os.path.join(BASE_DIR, "recruiter_outreach_tracker.json")

# Verified message templates customized for Vansh
TEMPLATES = {
    "recruiter_email": """Subject: MCA AI Graduate / {role} Application - Vansh Sharma

Hi {recruiter_name},

I hope you are having a productive week.

I came across the {role} position at {company} and wanted to reach out directly. I am completing my MCA in AI and Data Science (Class of 2026), with hands-on experience developing agentic workflows and retrieval systems.

A quick snapshot of relevant work:
- ResearchMind: Multi-agent arXiv intelligence system built with LangGraph, PyTorch, and hybrid BM25/FAISS retrieval.
- LexAI: End-to-end legal intelligence platform with verifiable source attribution, sub-200ms API response, and 0 hallucinations.

I would love the opportunity to contribute to {company}'s engineering initiatives. My resume is attached, and my portfolio projects can be reviewed at github.com/Vansh-Sharmaa.

Are you open to a brief 10-minute introductory conversation this week?

Warm regards,
Vansh Sharma
engagevansh@gmail.com | +91 9310461877 | New Delhi, India
github.com/Vansh-Sharmaa | linkedin.com/in/vansh-sharma
""",

    "linkedin_inmail": """Hi {recruiter_name},

I saw your team is hiring for {role} at {company}. As an MCA AI & Data Science graduate (2026) building production-grade agentic AI pipelines with LangGraph, PyTorch, and FastAPI, I wanted to introduce myself directly.

Recently, I built ResearchMind (multi-agent autonomous paper synthesis with hybrid retrieval) and LexAI (legal assistant with exact source citations). 

I would welcome the chance to discuss how my practical AI engineering skill set aligns with your open requirements. Are you free for a quick chat?

Best regards,
Vansh Sharma
github.com/Vansh-Sharmaa
""",

    "hiring_manager_tech": """Subject: Practical AI Engineering for {company} - Vansh Sharma

Hi {recruiter_name},

I noticed your engineering team at {company} is tackling interesting challenges in {domain_or_tech}.

I am an AI engineer graduating in 2026 (MCA in AI and Data Science), focused on autonomous agent architectures, RAG optimization, and performant Python backends. In my recent project ResearchMind, I engineered multi-agent coordination using LangGraph and reduced context retrieval noise by 35% through custom rerankers.

I have attached my tailored resume for your review. If your team has 10 minutes, I would appreciate the chance to discuss how I can immediately add value to your current sprint goals.

Best regards,
Vansh Sharma
engagevansh@gmail.com | +91 9310461877
"""
}

def generate_outreach_pitch(company, role, recruiter_name="Hiring Team", channel="email", extra_context=""):
    clean_company = company.replace("\u2014", " - ").replace("\u2013", " - ").strip()
    clean_role = role.replace("\u2014", " - ").replace("\u2013", " - ").strip()
    clean_recruiter = recruiter_name.replace("\u2014", " - ").replace("\u2013", " - ").strip() or "Hiring Team"
    
    if channel == "inmail":
        template = TEMPLATES["linkedin_inmail"]
    elif channel == "manager":
        template = TEMPLATES["hiring_manager_tech"]
    else:
        template = TEMPLATES["recruiter_email"]

    pitch = template.format(
        company=clean_company,
        role=clean_role,
        recruiter_name=clean_recruiter,
        domain_or_tech=extra_context or "production AI and software development"
    )

    # Double-check 0 em-dashes
    pitch = pitch.replace("\u2014", " - ").replace("\u2013", " - ")

    subject = ""
    lines = pitch.strip().split("\n")
    if lines[0].startswith("Subject: "):
        subject = lines[0].replace("Subject: ", "").strip()
        body = "\n".join(lines[1:]).strip()
    else:
        subject = f"{clean_role} Opportunity - Vansh Sharma"
        body = pitch.strip()

    return {
        "subject": subject,
        "body": body,
        "full_text": pitch,
        "company": clean_company,
        "role": clean_role,
        "recruiter_name": clean_recruiter,
        "channel": channel
    }

def log_outreach(company, role, recruiter_name, contact_info, channel, status="Drafted"):
    item = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "company": company,
        "role": role,
        "recruiter_name": recruiter_name,
        "contact_info": contact_info,
        "channel": channel,
        "status": status
    }
    existing = []
    if os.path.exists(OUTREACH_TRACKER):
        try:
            with open(OUTREACH_TRACKER, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = []
    existing.append(item)
    with open(OUTREACH_TRACKER, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)
    return item

def get_outreach_history():
    if os.path.exists(OUTREACH_TRACKER):
        try:
            with open(OUTREACH_TRACKER, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

if __name__ == "__main__":
    out = generate_outreach_pitch("Amlgo Labs", "AI Engineer", "Priya", "email")
    print("Sample Cold Outreach Generated:")
    print("Subject:", out["subject"])
    print("Body preview:\n", out["body"][:250])
