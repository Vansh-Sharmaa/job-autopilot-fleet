"""
Multi-Agent Fleet Swarm Coordinator
Runs 4-5 specialized agents in parallel across LinkedIn, foundit, Cutshort, and Hirist.
"""
import sys
import os
import time
import subprocess
import threading
from datetime import datetime

BASE_DIR = r"D:\opencode stuff\job-agents"
TRACKER_PATH = os.path.join(BASE_DIR, "job_applications_tracker.csv")

def log(agent_tag, msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{agent_tag}] {msg}", flush=True)

def run_linkedin_agent():
    log("AGENT-LINKEDIN", "Starting Safe LinkedIn Easy Apply agent (0-2 YOE AI & Operations)...")
    cmd = f'python -u "{os.path.join(BASE_DIR, "linkedin_runner.py")}" 5 "AI Engineer"'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="ignore")
    for line in iter(p.stdout.readline, ''):
        if not line:
            break
        log("AGENT-LINKEDIN", line.strip())
    p.stdout.close()
    p.wait()
    log("AGENT-LINKEDIN", "LinkedIn agent batch completed.")

def run_foundit_agent():
    log("AGENT-FOUNDIT", "Starting foundit Mass Apply Engine...")
    cmd = f'python -u "{os.path.join(BASE_DIR, "foundit_mass_engine.py")}"'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="ignore")
    for line in iter(p.stdout.readline, ''):
        if not line:
            break
        log("AGENT-FOUNDIT", line.strip())
    p.stdout.close()
    p.wait()
    log("AGENT-FOUNDIT", "foundit engine batch completed.")

def run_orca_hunter_agent():
    log("AGENT-ORCA", "Launching Orca Autonomous Agent across Cutshort & Hirist...")
    prompt = (
        "Execute safe fresher job hunting protocol for Vansh Sharma (0-2 YOE). "
        "Search Cutshort (cutshort.io) and Hirist (hirist.tech) for active AI Engineer and Python roles. "
        "Apply to 3 verified matching positions, confirm 'Application sent' on DOM, append to D:\\opencode stuff\\job-agents\\job_applications_tracker.csv, and close tabs cleanly. Zero em-dashes."
    )
    cmd = f'orca agent launch --agent claude --worktree "path:C:\\Users\\XALTA\\.orca\\bots\\job-hunter" --prompt "{prompt}" --json'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="ignore")
    for line in iter(p.stdout.readline, ''):
        if not line:
            break
        log("AGENT-ORCA", line.strip())
    p.stdout.close()
    p.wait()
    log("AGENT-ORCA", "Orca agent session dispatched and working in background.")

def run_operations_agent():
    log("AGENT-OPERATIONS", "Starting Operations Roles Agent (Tech Ops, AI Ops 0-2 YOE)...")
    cmd = f'python -u "{os.path.join(BASE_DIR, "linkedin_runner.py")}" 3 "Operations Associate"'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="ignore")
    for line in iter(p.stdout.readline, ''):
        if not line:
            break
        log("AGENT-OPERATIONS", line.strip())
    p.stdout.close()
    p.wait()
    log("AGENT-OPERATIONS", "Operations agent batch completed.")

def main():
    print("=" * 65, flush=True)
    log("SWARM-CORE", "Initializing 4-Agent Distributed Job Hunting Swarm...")
    print("=" * 65, flush=True)

    threads = [
        threading.Thread(target=run_linkedin_agent, name="Thread-LinkedIn"),
        threading.Thread(target=run_foundit_agent, name="Thread-foundit"),
        threading.Thread(target=run_orca_hunter_agent, name="Thread-Orca"),
        threading.Thread(target=run_operations_agent, name="Thread-Operations")
    ]

    for t in threads:
        t.start()
        time.sleep(2) # stagger launches slightly to prevent CPU spikes

    for t in threads:
        t.join()

    print("=" * 65, flush=True)
    log("SWARM-CORE", "All 4 agents finished their runs. Applications logged to tracker.")
    print("=" * 65, flush=True)

if __name__ == "__main__":
    main()
