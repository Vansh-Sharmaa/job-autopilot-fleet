"""
Zero-Ban Safe LinkedIn Easy Apply Runner for Vansh Sharma
Executes human-paced 0-2 YOE Easy Apply applications via browse CLI.
"""
import sys
import os
import time
import json
import csv
import subprocess
from datetime import datetime

TRACKER_PATH = r"D:\opencode stuff\job-agents\job_applications_tracker.csv"
SEARCH_URL = "https://www.linkedin.com/jobs/search/?keywords=AI%20Engineer&location=India&f_AL=true&f_E=1,2&sortBy=DD"

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)

def get_applied_urls():
    applied = set()
    if os.path.exists(TRACKER_PATH):
        try:
            with open(TRACKER_PATH, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    url = r.get("url", "").strip()
                    if url:
                        # Normalize LinkedIn job ID
                        applied.add(url.rstrip("/"))
        except Exception as e:
            log(f"Error reading tracker: {e}")
    return applied

def append_tracker(company, role, location, url):
    today = datetime.now().strftime("%Y-%m-%d")
    row = [today, company, role, location, "LinkedIn", "Submitted", url]
    try:
        with open(TRACKER_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        log(f"Logged to tracker: {company} - {role}")
    except Exception as e:
        log(f"Failed to log to tracker: {e}")

def run_js(code, tab_id=None):
    script_path = r"D:\opencode stuff\job-agents\_temp_runner.js"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code)
    
    cmd = ["browse", "execute", "--file", script_path]
    if tab_id:
        cmd.extend(["--tab", str(tab_id)])
        
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    out = res.stdout.strip()
    
    # Try to parse json from stdout
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                return json.loads(line)
            except:
                pass
    return {"raw": out}

def main():
    target_count = 5
    keyword = "AI Engineer"
    if len(sys.argv) > 1:
        try:
            target_count = int(sys.argv[1])
        except:
            pass
    if len(sys.argv) > 2:
        keyword = sys.argv[2]

    import urllib.parse
    encoded_kw = urllib.parse.quote(keyword)
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_kw}&location=India&f_AL=true&f_E=1,2&sortBy=DD"

    log(f"Starting Safe LinkedIn Easy Apply batch for '{keyword}' (Target: {target_count} jobs)...")
    
    # Check open tabs
    tabs_res = subprocess.run(["browse", "tabs"], shell=True, capture_output=True, text=True)
    tab_id = None
    try:
        tabs_data = json.loads(tabs_res.stdout)
        for t in tabs_data.get("tabs", []):
            if "linkedin.com" in t.get("url", ""):
                tab_id = t.get("tab")
                break
    except:
        pass

    if not tab_id:
        log(f"Opening new tab for LinkedIn search: {search_url}...")
        nav_res = subprocess.run(["browse", "navigate", search_url], shell=True, capture_output=True, text=True)
        try:
            nav_data = json.loads(nav_res.stdout)
            tab_id = nav_data.get("tab")
        except:
            log(f"Navigate output: {nav_res.stdout}")
    else:
        log(f"Reusing existing LinkedIn tab {tab_id} for {keyword}...")
        subprocess.run(["browse", "navigate", search_url, "--tab", str(tab_id)], shell=True, capture_output=True)

    time.sleep(4)
    applied_urls = get_applied_urls()
    log(f"Deduplication cache loaded: {len(applied_urls)} total prior applications.")

    applied_in_batch = 0

    # Script to get visible job cards
    get_jobs_js = """
    async (page) => {
        await page.waitForTimeout(3000);
        const cards = await page.$$eval('li[data-occludable-job-id], .jobs-search-results__list-item', els => els.map(el => {
            const titleEl = el.querySelector('a.job-card-list__title--link, a.job-card-container__link, strong');
            const compEl = el.querySelector('.artdeco-entity-lockup__subtitle, .job-card-container__primary-description');
            const locEl = el.querySelector('.artdeco-entity-lockup__caption, .job-card-container__metadata-item');
            const link = titleEl ? titleEl.href : '';
            return {
                title: titleEl ? titleEl.innerText.trim() : '',
                company: compEl ? compEl.innerText.trim() : '',
                location: locEl ? locEl.innerText.trim() : 'India',
                url: link ? link.split('?')[0] : '',
                jobId: el.getAttribute('data-occludable-job-id') || ''
            };
        }));
        return { count: cards.length, cards };
    }
    """

    res = run_js(get_jobs_js, tab_id)
    cards = res.get("cards", [])
    log(f"Found {len(cards)} job cards in current search view.")

    # Process cards
    for card in cards:
        if applied_in_batch >= target_count:
            log(f"Reached safe target of {target_count} LinkedIn applications.")
            break

        url = card.get("url", "")
        title = card.get("title", "")
        company = card.get("company", "")
        loc = card.get("location", "India")
        job_id = card.get("jobId", "")

        if not url or url in applied_urls:
            continue

        log(f"Evaluating: {company} | {title}...")

        # Navigate to job view
        job_url = f"https://www.linkedin.com/jobs/view/{job_id}/" if job_id else url
        subprocess.run(["browse", "navigate", job_url, "--tab", str(tab_id)], shell=True, capture_output=True)
        time.sleep(3)

        # Apply script
        apply_flow_js = """
        async (page) => {
            await page.waitForTimeout(2000);
            
            // Check if already applied
            const bodyText = document.body.innerText;
            if (bodyText.includes("Application submitted") || bodyText.includes("Applied")) {
                return { status: "already_applied" };
            }

            // Find Easy Apply button
            const applyBtn = Array.from(document.querySelectorAll('button')).find(b => {
                const t = (b.innerText || '').trim();
                return t.includes("Easy Apply");
            });

            if (!applyBtn) {
                return { status: "no_easy_apply" };
            }

            applyBtn.click();
            await page.waitForTimeout(2000);

            // Step loop (max 4 steps)
            for (let step = 0; step < 5; step++) {
                const text = document.body.innerText;
                
                // If submitted confirmation
                if (text.includes("Application sent") || text.includes("Your application was sent")) {
                    const dismiss = Array.from(document.querySelectorAll('button')).find(b => {
                        const t = (b.innerText || b.getAttribute('aria-label') || '').toLowerCase();
                        return t.includes('dismiss') || t.includes('done');
                    });
                    if (dismiss) dismiss.click();
                    return { status: "submitted" };
                }

                const modal = document.querySelector('.jobs-easy-apply-modal, [role="dialog"]') || document.body;
                
                // Smart Human-Written Question Answering Engine
                const getSmartAnswer = (label, isTextarea) => {
                    const p = (label || '').toLowerCase();
                    if (p.includes('authorized to work') || p.includes('legally authorized') || p.includes('right to work')) return 'Yes';
                    if (p.includes('sponsorship') || p.includes('require visa') || p.includes('future require')) return 'No';
                    if (p.includes('relocate') || p.includes('comfortable') || p.includes('immediate') || p.includes('remote') || p.includes('hybrid')) return 'Yes';
                    if (p.includes('notice') || p.includes('days')) return '0';
                    if (p.includes('current ctc') || p.includes('current salary')) return '0';
                    if (p.includes('expected ctc') || p.includes('expected salary')) return '600000';
                    if (p.includes('cgpa') || p.includes('gpa')) return '8.0';
                    if (p.includes('python') || p.includes('git')) return '3';
                    if (p.includes('pytorch') || p.includes('fastapi') || p.includes('sql') || p.includes('c++') || p.includes('machine learning') || p.includes('ml')) return '2';
                    if (p.includes('langgraph') || p.includes('langchain') || p.includes('docker') || p.includes('rag') || p.includes('vector') || p.includes('agent')) return '1';
                    
                    if (p.includes('why do you') || p.includes('why join') || p.includes('interested')) {
                        return "I have been tracking what your team is building with applied AI, and I want to work somewhere engineering quality and shipping fast matter more than bureaucracy. My background is in production RAG systems, LangGraph agent workflows, and ML feature pipelines. I want to jump in, take ownership of technical challenges, and build reliable software that users actually use.";
                    }
                    if (p.includes('llm') || p.includes('genai') || p.includes('generative ai') || (isTextarea && p.includes('experience'))) {
                        return "I build multi-agent systems and RAG pipelines end-to-end. In ResearchMind, I built a LangGraph state graph orchestrating 4 specialized agents (Search, Scrape, Writer, Critic) with automated reflection loops. In LexAI, I implemented a Map-Reduce summarization chain for legal contracts and FAISS semantic vector search with all-MiniLM-L6-v2 embeddings to ground LLM outputs and eliminate hallucinations.";
                    }
                    if (p.includes('challenge') || p.includes('difficult') || p.includes('project')) {
                        return "I built FileGenie, a content-based file classification and security engine. Traditional tools only check file extensions, which fails when executables are renamed to .pdf. I built a 16-dimensional feature extraction pipeline calculating Shannon Entropy, raw binary magic bytes, and null-byte distributions, training a 300-tree Random Forest classifier in scikit-learn that achieves 95%+ accuracy in under 1ms on CPU, integrated with high-throughput FastAPI streaming.";
                    }
                    if (isTextarea) {
                        return "I am an AI/ML Engineer completing my MCA in AI & Data Science. I focus on practical GenAI: multi-agent orchestration in LangGraph, Retrieval-Augmented Generation with vector databases, and full-stack deployment using FastAPI and Python. I prefer building working prototypes and reliable pipelines over just calling standard API endpoints.";
                    }
                    return '1';
                };

                // Fill inputs intelligently
                const inputs = Array.from(modal.querySelectorAll('input[type="text"], input[type="number"], textarea'));
                inputs.forEach(i => {
                    if (!i.value || i.value.trim() === '') {
                        const parentLabel = i.closest('div')?.innerText || i.getAttribute('aria-label') || '';
                        const ans = getSmartAnswer(parentLabel, i.tagName.toLowerCase() === 'textarea');
                        i.value = ans;
                        i.dispatchEvent(new Event('input', { bubbles: true }));
                        i.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                });

                // Handle unselected radio buttons
                const radioGroups = Array.from(modal.querySelectorAll('fieldset, [role="radiogroup"]'));
                radioGroups.forEach(rg => {
                    const label = rg.innerText || '';
                    const ans = getSmartAnswer(label, false);
                    const radios = Array.from(rg.querySelectorAll('input[type="radio"], [role="radio"]'));
                    const targetRadio = radios.find(r => {
                        const rText = r.closest('label')?.innerText || r.value || '';
                        return rText.toLowerCase().includes(ans.toLowerCase());
                    });
                    if (targetRadio && !targetRadio.checked) targetRadio.click();
                });

                // Check for Submit Application button
                const submitBtn = Array.from(modal.querySelectorAll('button')).find(b => {
                    const t = (b.innerText || '').toLowerCase();
                    return t.includes("submit application");
                });

                if (submitBtn) {
                    submitBtn.click();
                    await page.waitForTimeout(3000);
                    const afterSubmitText = document.body.innerText;
                    if (afterSubmitText.includes("Application sent") || afterSubmitText.includes("Your application was sent")) {
                        const dismiss = Array.from(document.querySelectorAll('button')).find(b => {
                            const t = (b.innerText || b.getAttribute('aria-label') || '').toLowerCase();
                            return t.includes('dismiss') || t.includes('done');
                        });
                        if (dismiss) dismiss.click();
                        return { status: "submitted" };
                    }
                }

                // Check for Review button
                const reviewBtn = Array.from(modal.querySelectorAll('button')).find(b => (b.innerText || '').trim() === "Review");
                if (reviewBtn) {
                    reviewBtn.click();
                    await page.waitForTimeout(1500);
                    continue;
                }

                // Check for Next button
                const nextBtn = Array.from(modal.querySelectorAll('button')).find(b => (b.innerText || '').trim() === "Next");
                if (nextBtn) {
                    nextBtn.click();
                    await page.waitForTimeout(1500);
                    continue;
                }

                break;
            }

            // If we are stuck on a multi-page essay form, discard
            const closeBtn = Array.from(document.querySelectorAll('button')).find(b => {
                const aria = (b.getAttribute('aria-label') || '').toLowerCase();
                return aria.includes('dismiss') || aria.includes('close');
            });
            if (closeBtn) {
                closeBtn.click();
                await page.waitForTimeout(500);
                const discardBtn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').toLowerCase().includes('discard'));
                if (discardBtn) discardBtn.click();
            }

            return { status: "discarded_or_skipped" };
        }
        """

        flow_res = run_js(apply_flow_js, tab_id)
        res_status = flow_res.get("status", "")

        if res_status == "submitted":
            log(f"SUCCESS: Submitted {company} ({title})!")
            append_tracker(company, title, loc, job_url)
            applied_urls.add(job_url)
            applied_in_batch += 1
            log("Pacing: pausing 18 seconds for account safety...")
            time.sleep(18)
        else:
            log(f"Skipped {company} ({res_status})")
            time.sleep(3)

    log(f"LinkedIn batch finished. Successfully submitted {applied_in_batch} applications.")

if __name__ == "__main__":
    main()
