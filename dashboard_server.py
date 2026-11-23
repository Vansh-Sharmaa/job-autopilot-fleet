"""
Job Application Mission Control & Automation Dashboard
Lightweight local web server with 1-click execution and live tracking.
"""
import sys
import os
import time
import json
import csv
import subprocess
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import screening_engine
import quota_manager
import ats_engine
import recruiter_dispatcher
import assessment_prep_engine

PORT = 5055
BASE_DIR = r"D:\opencode stuff\job-agents"
TRACKER_PATH = os.path.join(BASE_DIR, "job_applications_tracker.csv")

# Global process management
active_process = None
active_task_name = "None"
task_logs = []
process_lock = threading.Lock()

def add_log(msg):
    global task_logs
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with process_lock:
        task_logs.append(line)
        if len(task_logs) > 300:
            task_logs.pop(0)

def read_stats():
    rows = []
    if os.path.exists(TRACKER_PATH):
        try:
            with open(TRACKER_PATH, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    if r.get("company") or r.get("role"):
                        rows.append(r)
        except Exception as e:
            add_log(f"Error reading tracker: {e}")

    today = datetime.now().strftime("%Y-%m-%d")
    today_rows = [r for r in rows if r.get("date") == today]

    portals = {}
    for r in rows:
        p = r.get("portal", "Other").strip()
        if not p or p.startswith("http"):
            p = "Instahyre" if "instahyre" in p.lower() else "Portal"
        portals[p] = portals.get(p, 0) + 1

    today_portals = {}
    for r in today_rows:
        p = r.get("portal", "Other").strip()
        if not p or p.startswith("http"):
            p = "Instahyre" if "instahyre" in p.lower() else "Portal"
        today_portals[p] = today_portals.get(p, 0) + 1

    return {
        "total_all_time": len(rows),
        "total_today": len(today_rows),
        "portals": portals,
        "today_portals": today_portals,
        "quotas": quota_manager.get_quota_overview(),
        "recent": rows[-25:][::-1],
        "is_running": active_process is not None and active_process.poll() is None,
        "active_task": active_task_name
    }

def worker_thread(cmd, task_name):
    global active_process, active_task_name
    add_log(f"Starting task: {task_name}")
    try:
        active_process = subprocess.Popen(
            cmd,
            cwd=BASE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="ignore",
            bufsize=1
        )
        for line in iter(active_process.stdout.readline, ''):
            if not line:
                break
            add_log(line.strip())
        active_process.stdout.close()
        active_process.wait()
        add_log(f"Completed task: {task_name} (Code: {active_process.returncode})")
    except Exception as e:
        add_log(f"Task error ({task_name}): {e}")
    finally:
        with process_lock:
            active_process = None
            active_task_name = "None"

class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress default noisy console logs

    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html_path = os.path.join(BASE_DIR, "dashboard.html")
            if os.path.exists(html_path):
                with open(html_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"<h1>Dashboard file not found</h1>")
            return

        if path == "/api/stats":
            self.send_json(read_stats())
            return

        if path == "/api/logs":
            with process_lock:
                logs_copy = list(task_logs)
            is_run = active_process is not None and active_process.poll() is None
            self.send_json({"logs": logs_copy, "is_running": is_run, "active_task": active_task_name})
            return

        if path == "/api/interviews":
            tracker_file = os.path.join(BASE_DIR, "interviews_tracker.json")
            items = []
            if os.path.exists(tracker_file):
                try:
                    with open(tracker_file, "r", encoding="utf-8") as f:
                        items = json.load(f)
                except Exception as e:
                    items = []

            # Compute category and account breakdowns
            shortlisted_count = len([x for x in items if x.get("category") == "SHORTLISTED"])
            assessment_count = len([x for x in items if x.get("category") == "ASSESSMENT"])
            interview_count = len([x for x in items if x.get("category") == "INTERVIEW"])

            by_account = {}
            for x in items:
                acc = x.get("account", "Other")
                by_account[acc] = by_account.get(acc, 0) + 1

            self.send_json({
                "interviews": items,
                "count": len(items),
                "metrics": {
                    "shortlisted": shortlisted_count,
                    "assessments": assessment_count,
                    "interviews": interview_count,
                    "by_account": by_account
                }
            })
            return

        if path == "/api/outreach-history":
            self.send_json({"history": recruiter_dispatcher.get_outreach_history()})
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        global active_process, active_task_name
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""
        data = {}
        if body:
            try:
                data = json.loads(body)
            except:
                pass

        if path == "/api/test-screening":
            q = data.get("question", "")
            opts = data.get("options", None)
            ans = screening_engine.answer_question(q, opts)
            self.send_json({"question": q, "answer": ans})
            return

        if path == "/api/ats-score":
            jd = data.get("jd", "")
            role = data.get("role", "AI Engineer")
            res = ats_engine.calculate_ats_score(jd, role)
            self.send_json(res)
            return

        if path == "/api/tailor-resume":
            comp = data.get("company", "Tech Company")
            role = data.get("role", "AI Engineer")
            jd = data.get("jd", "")
            res = ats_engine.generate_tailored_resume_for_job(comp, role, jd)
            self.send_json({"success": True, "result": res})
            return

        if path == "/api/generate-outreach":
            comp = data.get("company", "")
            role = data.get("role", "AI Engineer")
            recruiter = data.get("recruiter_name", "Hiring Team")
            channel = data.get("channel", "email")
            context = data.get("context", "")
            pitch = recruiter_dispatcher.generate_outreach_pitch(comp, role, recruiter, channel, context)
            self.send_json({"success": True, "pitch": pitch})
            return

        if path == "/api/log-outreach":
            comp = data.get("company", "")
            role = data.get("role", "")
            recruiter = data.get("recruiter_name", "")
            contact = data.get("contact_info", "")
            channel = data.get("channel", "email")
            logged = recruiter_dispatcher.log_outreach(comp, role, recruiter, contact, channel, "Sent")
            self.send_json({"success": True, "entry": logged})
            return

        if path == "/api/solve-dsa":
            prob = data.get("problem", "")
            lang = data.get("language", "python")
            sol = assessment_prep_engine.generate_dsa_solution(prob, lang)
            self.send_json({"success": True, "solution": sol})
            return

        if path == "/api/prep-kit":
            comp = data.get("company", "Tech Company")
            role = data.get("role", "AI Engineer")
            provider = data.get("provider", "HackerEarth")
            kit = assessment_prep_engine.generate_prep_kit(comp, role, provider)
            self.send_json({"success": True, "kit": kit})
            return

        if path == "/api/scan-interviews":
            with process_lock:
                if active_process is not None and active_process.poll() is None:
                    self.send_json({"success": False, "error": f"A task is already running: {active_task_name}"})
                    return
                cmd = [sys.executable, "-u", os.path.join(BASE_DIR, "gmail_scanner.py")]
                task_title = "Inbound Gmail Assessment & Interview Scanner"
                active_task_name = task_title
                t = threading.Thread(target=worker_thread, args=(cmd, task_title), daemon=True)
                t.start()
            self.send_json({"success": True, "task": task_title})
            return

        if path == "/api/run":
            with process_lock:
                if active_process is not None and active_process.poll() is None:
                    self.send_json({"success": False, "error": f"A task is already running: {active_task_name}"})
                    return

                target = data.get("target", "linkedin")
                if target == "autopilot":
                    cmd = [sys.executable, "-u", os.path.join(BASE_DIR, "daily_autopilot_daemon.py")]
                    task_title = "Daily Auto-Pilot 24/7 Master Daemon"
                elif target == "inbound_email_calendar" or target == "calendar":
                    cmd = [sys.executable, "-u", os.path.join(BASE_DIR, "inbound_email_calendar_runner.py")]
                    task_title = "Inbound Email Alerts & Calendar Jobs Auto-Apply"
                elif target == "fill_all" or target == "maximize_all":
                    cmd = [sys.executable, "-u", os.path.join(BASE_DIR, "fill_all_quotas.py")]
                    task_title = "Daily Quota Maximizer (Fill All 13 Platforms)"
                elif target == "swarm" or target == "mega_swarm":
                    cmd = [sys.executable, "-u", os.path.join(BASE_DIR, "mega_swarm_all_platforms.py")]
                    task_title = "Mega-Swarm (All Platforms: LinkedIn + foundit + Orca + Hasjob + Instahyre)"
                elif target == "linkedin":
                    cmd = [sys.executable, "-u", os.path.join(BASE_DIR, "linkedin_runner.py"), "5", "AI Engineer"]
                    task_title = "LinkedIn Easy Apply (5 AI Engineer Jobs)"
                elif target == "operations":
                    cmd = [sys.executable, "-u", os.path.join(BASE_DIR, "linkedin_runner.py"), "5", "Operations Associate"]
                    task_title = "Operations Roles Easy Apply (Tech Ops, AI Ops, 0-2 YOE)"
                elif target == "orca":
                    prompt = "Execute safe fresher job hunting protocol for Vansh Sharma. Search 0-2 YOE AI / Python roles on Cutshort and Hirist. Max 5 applications, confirm submission, zero em-dashes."
                    cmd = [
                        "orca", "agent", "launch", "--agent", "claude",
                        "--worktree", r"path:C:\Users\XALTA\.orca\bots\job-hunter",
                        "--prompt", prompt, "--json"
                    ]
                    task_title = "Orca Job Hunter Autonomous Run"
                elif target == "cutshort":
                    prompt = "Open Cutshort jobs dashboard. Apply to 5 matching 0-2 YOE AI / Python developer roles. Auto-fill 0 years full-time, 6 months internship, 0 current CTC, 6 LPA expected CTC. Confirm submission and log."
                    cmd = [
                        "orca", "agent", "launch", "--agent", "claude",
                        "--worktree", r"path:C:\Users\XALTA\.orca\bots\job-hunter",
                        "--prompt", prompt, "--json"
                    ]
                    task_title = "Cutshort Autonomous Batch"
                elif target == "hirist":
                    prompt = "Open hirist.tech jobs for AI Engineer and Python Developer (0-2 YOE). Fill screening questions (Python: 1 yr, ML: 1 yr, CTC: 0, Expected: 6 LPA) and submit 3 verified applications."
                    cmd = [
                        "orca", "agent", "launch", "--agent", "claude",
                        "--worktree", r"path:C:\Users\XALTA\.orca\bots\job-hunter",
                        "--prompt", prompt, "--json"
                    ]
                    task_title = "Hirist Tech Batch"
                elif target == "unstop":
                    cmd = [sys.executable, "-u", os.path.join(BASE_DIR, "extended_platforms_runner.py"), "unstop"]
                    task_title = "Unstop Fresher Tech Challenges"
                elif target == "cuvette":
                    cmd = [sys.executable, "-u", os.path.join(BASE_DIR, "extended_platforms_runner.py"), "cuvette"]
                    task_title = "Cuvette 0-2 YOE Tech Roles"
                elif target == "wellfound":
                    cmd = [sys.executable, "-u", os.path.join(BASE_DIR, "extended_platforms_runner.py"), "wellfound"]
                    task_title = "Wellfound (AngelList) AI Startups"
                elif target == "yc":
                    cmd = [sys.executable, "-u", os.path.join(BASE_DIR, "extended_platforms_runner.py"), "yc"]
                    task_title = "Y Combinator Work at a Startup"
                elif target == "indeed":
                    cmd = [sys.executable, "-u", os.path.join(BASE_DIR, "extended_platforms_runner.py"), "indeed"]
                    task_title = "Indeed India Entry-Level Apply"
                elif target == "foundit":
                    cmd = [sys.executable, "-u", os.path.join(BASE_DIR, "foundit_mass_engine.py")]
                    task_title = "foundit (Monster) Mass Engine"
                elif target == "fleet":
                    cmd = [sys.executable, "-u", os.path.join(BASE_DIR, "fleet_scale_150.py")]
                    task_title = "Full Multi-Platform Fleet"
                else:
                    self.send_json({"success": False, "error": f"Unknown target: {target}"})
                    return

                active_task_name = task_title
                t = threading.Thread(target=worker_thread, args=(cmd, task_title), daemon=True)
                t.start()

            self.send_json({"success": True, "task": task_title})
            return

        if path == "/api/stop":
            with process_lock:
                if active_process is not None and active_process.poll() is None:
                    active_process.terminate()
                    add_log("Received abort signal: Terminating active task...")
                    active_process = None
                    active_task_name = "None"
                    self.send_json({"success": True, "message": "Task stopped"})
                    return
            self.send_json({"success": False, "message": "No active task to stop"})
            return

        self.send_response(404)
        self.end_headers()

def run_server():
    server_address = ("127.0.0.1", PORT)
    httpd = HTTPServer(server_address, DashboardHandler)
    add_log(f"Mission Control Server active at http://127.0.0.1:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == "__main__":
    run_server()
