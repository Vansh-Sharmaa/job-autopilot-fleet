# Job-Application Playbook (browser)

The universal apply loop every agent runs. Browser calls are the tools in the harness
(`tools.browse.*`: navigate, snapshot, click, fill, press, scroll, wait_for, eval).

## 0. Setup

- One tab per agent. To run agent N: open its Search URL (its spec) in a tab and run the loop below.

## 1. Open the search

`tools.browse.navigate({ tab, url })` to the spec's Search URL. If a matching tab is already open,
reuse it (`tools.browse.status` lists open tabs).

## 2. Snapshot the results page & Strict Relevance Check

`tools.browse.snapshot({ tab })` returns the accessibility tree; job cards appear as buttons with
titles, e.g.
`- button "AI Engineer TerraTern Bengaluru (On-site) Dismiss AI Engineer job Viewed · Easy Apply" [ref=e135]`.

**MANDATORY RELEVANCE FILTER (Based on `D:\improved resume\Vansh_Sharma_Resume.pdf`):**
A card is an **APPLY TARGET** only if:
1. Title matches target roles: AI Engineer, GenAI, Machine Learning, Python AI Developer, LLM/RAG Engineer.
2. Experience matches candidate profile: 0–2 years / Entry level / Associate. (Skip anything saying 3+, 5+ years).
3. The card does **NOT** already show status **Applied**.
4. Disqualify irrelevant roles: Java/C# only, Sales, Marketing, Customer Support, Unpaid.

(Newest first is typical; scroll with `tools.browse.scroll` if you hit the bottom, then re-snapshot.)

## 3. Open the job card

`tools.browse.click({ tab, ref })` on the matching card. Snapshot again. Find the job's apply
button: **"Easy Apply to this job"** (`ref=e179` style). If the card shows **Applied**, skip it. If
there is no Easy Apply button, skip the job (log `skipped: no easy apply`).

## 4. Fill the application form

Click **"Easy Apply to this job"**. Snapshot the dialog:
- Fill fields with the values in `data.md` (name, email, phone, links, answers).
- **DYNAMIC RESUME TAILORING (100% ATS Match):**
  Before uploading the resume, check the Job Description on the page:
  Run dynamic tailoring:
  `uv run --with reportlab --with pypdf "D:\improved resume\tailor_resume.py" --company "<Company>" --role "<Role>" --jd "<JD snippet>"`
  It generates a verified 1-page tailored PDF in `D:\improved resume\tailored\`.
  Upload this tailored PDF.
  (Fallback: `D:\improved resume\Vansh_Sharma_Resume.pdf`).
- Fields with reasonable defaults (location, availability) can be filled or left.

## 5. Submit

Find the submit button ("Apply", "Submit application", "Send application") and
`tools.browse.click` it.

## 6. Verify & Tab Cleanup (MANDATORY RAM MANAGEMENT)

1. `tools.browse.snapshot({ tab })` - look for the card now showing **Applied**, or a success message ("Your application was sent").
2. **IMMEDIATELY CLOSE THE TAB:**
   - As soon as the application is verified (or if a job is skipped/failed), close that job's tab immediately (`await page.close()` or `tools.browse.tabs.close`).
   - NEVER keep completed or rejected job tabs open. Only the main search tab should stay alive.
   - At any time, maximum open tabs in the browser must be $\le 2$ to keep laptop RAM clean.

## 7. Log the result

Append one line to the agent's log file:

```
YYYY-MM-DD | <Company / card text> | <applied|skipped|failed|handoff> | <notes>
```

## 8. Pacing

Between jobs: a short pause (page loads/calls take a few seconds each). Stop the agent when:
- The spec's daily cap is reached, or
- 3+ consecutive failures/handoffs, or
- The user pauses the agent.

## Multi-site

Each agent spec lists its `Sites` and `Site notes`. The LinkedIn loop is the main flow. For other
boards (Indeed, etc.), the loop is the same: snapshot the site's search → click a matching card →
click the site's apply button ("full details of <Title>" → "Apply on company site" / "Apply") →
fill the site's application form → submit → verify → log. An agent works one site's tab at a time;
everything is recorded in the same log file.

## Handoff  -  stop and notify (human required)

Stop the agent and log `handoff: <reason>` when anything needs you:
- "We need you to log in", "Complete 2FA", "verify your phone", CAPTCHA, "something went wrong, try again later".
- A job requires a file/field that is not in `data.md` (e.g. a specific cover letter or a different resume).
- The results page shows a login or error wall.

Check the agent's log file and the LinkedIn "Application status" for what happened, then resume.
