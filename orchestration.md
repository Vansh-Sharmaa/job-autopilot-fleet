# Multi-AI Job Hunting Orchestration System

This system lets your AI agents (**Claude Code, Codex, OpenCode, Antigravity**) work together in parallel across multiple job platforms (**LinkedIn, Indeed, Wellfound, Y Combinator, Greenhouse**) without colliding or duplicate applications.

---

## 🏗️ Architecture

```
                               ┌────────────────────────────────────────────────────────┐
                               │             D:\opencode stuff\job-agents               │
                               │  data.md (Personal Info + Anti-AI Screening Answers)   │
                               │  Resume: D:\improved resume\Vansh_Sharma_Resume.pdf    │
                               └───────────────────────────┬────────────────────────────┘
                                                           │
                      ┌────────────────────────────────────┼────────────────────────────────────┐
                      ▼                                    ▼                                    ▼
          [Terminal 1: Claude Code]               [Terminal 2: Codex]                 [Terminal 3: OpenCode]
            Agent 1 (LinkedIn GenAI)             Agent 4 (Wellfound Startups)           Agent 5 (YC & ATS Portals)
            Agent 2 (LinkedIn RAG)               Agent 3 (Indeed Freshers)
                      │                                    │                                    │
                      └────────────────────────────────────┼────────────────────────────────────┘
                                                           ▼
                                      ┌────────────────────────────────────────┐
                                      │  Unified Browser Bridge (browse.exe)   │
                                      │  Brave / Chrome Tabs (Port 19988)      │
                                      └────────────────────────────────────────┘
```

---

## 🛡️ Zero-Mistake & Zero-AI Footprint Rules

### 1. Zero-AI Writing Rules (MANDATORY):
- **NO Em-Dashes (` - `):** Never use em-dashes or en-dashes anywhere in screening answers, notes, or resume files. Real engineers use standard commas, colons, or standard hyphens (`-`).
- **Banned AI Vocabulary:** Strictly eliminate words like *delve, testament, tapestry, spearhead, robust, seamless, seamlessly, leverage, leveraging, foster, beacon, pivotal, crucial, revolutionize, thrilled, esteemed, elevate, multifaceted, furthermore, moreover*.
- **Natural Engineer Tone:** Answers must be 2 to 3 sentences, written directly, subject-verb-object, mentioning real project features, latency metrics, and tools.

### 2. 4-Stage Zero-Mistake Pipeline:
- **Stage 1 (The Scout):** Filter for 0-2 YOE, Fresher, Associate only. Hard-skip 3+ years and non-technical roles.
- **Stage 2 (The Tailor):** Run `uv run --with reportlab --with pypdf "D:\improved resume\tailor_resume.py" --company "<Company>" --role "<Role>" --jd "<JD text>"` to compile a tailored 1-page PDF.
- **Stage 3 (The Inspector):** Verify: PDF exists & is 1 page, role is 0-2 years, no duplicate in CSV, no em-dashes in answers.
- **Stage 4 (The Submitter):** Fill browser form, attach tailored PDF, click submit, and append to `job_applications_tracker.csv`.

### 3. Pacing & Safety (Zero-Ban Platforms):
- Focus on Zero-Ban platforms: Simplify Jobs, Naukri, Indeed India, Instahyre, Hirist, foundit, Himalayas, Cutshort.
- 15–35 applications per platform per day (Distributed fleet for 200/day total).
- 15–30 second natural delays between actions.
- **Mandatory Tab Cleanup (Low RAM):** Immediately close the job tab after submission or skip (`await page.close()`). Never leave old tabs open. Maximum open tabs at any time must be <= 2 to keep laptop RAM clean and fast.

---

## 🚀 How to Launch Your Multi-AI Fleet

Open **3 separate Terminal windows**:

### Terminal 1  -  Run Claude Code (Handles LinkedIn Easy Apply):
```powershell
cd "D:\opencode stuff\job-agents"
claude
```
> **Prompt:** `"Run Agent 1 and Agent 2 from the agents/ folder. Open separate browser tabs via browse, find matching GenAI/RAG roles in India, fill details from data.md, attach D:\improved resume\Vansh_Sharma_Resume.pdf, and submit."`

---

### Terminal 2  -  Run Codex (Handles Wellfound & Indeed):
```powershell
cd "D:\opencode stuff\job-agents"
codex
```
> **Prompt:** `"Run Agent 4 (Wellfound) and Agent 3 (Indeed). Open browser tabs, find 0-2 year AI roles, fill forms with human answers from data.md section 6, and log results."`

---

### Terminal 3  -  Run OpenCode (Handles Y Combinator & Direct ATS):
```powershell
cd "D:\opencode stuff\job-agents"
opencode
```
> **Prompt:** `"Run Agent 5. Check Y Combinator and direct Greenhouse/Lever portals for AI Engineer roles in India / Remote, fill applications from data.md, and submit."`

---

## 📊 Daily Review
At the end of each session, review:
* `logs/agent-1.md` (LinkedIn GenAI)
* `logs/agent-2.md` (LinkedIn RAG)
* `logs/agent-3.md` (Indeed Freshers)
* `logs/agent-4.md` (Wellfound Startups)
* `logs/agent-5.md` (YC & Direct ATS)
