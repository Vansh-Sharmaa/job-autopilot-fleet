@echo off
title Job Hunting Daily Auto-Pilot Fleet - Vansh Sharma
cd /d "D:\opencode stuff\job-agents"
echo Starting Job Hunting Daily Auto-Pilot Master Daemon...
python -u daily_autopilot_daemon.py >> autopilot_daemon.log 2>&1
