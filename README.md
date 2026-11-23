# Job-Application Agents

Your agents that apply for jobs for you, driven in the browser. This folder is the system: your
profile data, the application playbook, one spec per agent, and the logs agents write to.

## What an "agent" is here

Each agent = an agent spec (`agents/agent-N.md`) + the browser loop in `playbook.md`. An agent:

1. Opens its search URL (LinkedIn style) — see the spec's `Search URL`.
2. Snapshots the results page and reads job cards with `tools.browse.snapshot`.
3. Skips cards whose status is already **Applied**; applies to matching cards: click the card →
   click the **"Easy Apply to this job"** button (LinkedIn) or the site's apply button (Indeed).
4. Fills the application form from `data.md` (name, email, phone, resume, …).
5. Clicks the submit button and verifies the card shows **Applied** (LinkedIn) or confirms the
   submission on the site.
6. Appends a log line to `logs/agent-N.md`.

## How to run them

- One tab per agent. To run agent N: open its spec, open its Search URL in a tab, then follow
  `playbook.md` — each step says which browser call to use.
- Run agents in parallel (agents 1, 2, 3 at the same time), or rotate them over time.
- When agents apply, review the logs (`logs/*.md`) daily, as agreed.

## Safety & review

See `playbook.md` (safety + handoff rules) and the per-agent caps in the specs:
- Agents pause and log for you to finish anything that needs a human (login, 2FA, CAPTCHA,
  payment, non-standard forms).
- Per-agent daily caps in the specs (defaults: 10 / 8 / 12).
- Human review of `logs/*.md` after each run.

## Files

| File | What it is |
|---|---|
| `data.md` | Your applicant profile used in applications |
| `playbook.md` | The universal browser loop: search → apply → verify → log (+ multi-site) |
| `agents/agent-N.md` | Per-agent: focus, criteria, search URL, tabs, caps, log file |
| `orchestration.md` | How to launch, run and monitor the agents |
| `logs/agent-N.md` | Results log — agents append here |
