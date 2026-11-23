import sys
import csv
import os

TRACKER_FILE = r"D:\opencode stuff\job-agents\job_applications_tracker.csv"

def lookup_company(query):
    if not os.path.exists(TRACKER_FILE):
        print("Tracker file not found!")
        return
    
    query = query.lower().strip()
    matches = []
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            comp = row.get("company", "").lower()
            role = row.get("role", "").lower()
            if query in comp or query in role:
                matches.append(row)
                
    if not matches:
        print(f"No match found for: '{query}'")
        return
        
    print("\n" + "="*60)
    print(f" FOUND {len(matches)} APPLICATION(S) MATCHING: '{query}'")
    print("="*60)
    for m in matches:
        print(f"Company:   {m.get('company')}")
        print(f"Role:      {m.get('role')}")
        print(f"Location:  {m.get('location')}")
        print(f"Portal:    {m.get('portal')}")
        print(f"Date:      {m.get('date')}")
        print(f"Status:    {m.get('status')}")
        print(f"Job Link:  {m.get('url')}")
        print("-" * 60)
        
        # Smart interview cheat sheet
        role_lower = m.get('role', '').lower()
        print("💡 QUICK INTERVIEW TALKING POINTS:")
        if "agent" in role_lower or "genai" in role_lower or "llm" in role_lower or "rag" in role_lower:
            print("  -> Anchor on: 'ResearchMind' (4-agent LangGraph system with cycle-detection)")
            print("  -> Anchor on: 'LexAI' (FAISS vector search, Map-Reduce summarization)")
        elif "vision" in role_lower or "fastapi" in role_lower or "machine learning" in role_lower:
            print("  -> Anchor on: 'FileGenie' (300-tree Random Forest, Shannon Entropy, FastAPI <1ms latency)")
        else:
            print("  -> Anchor on: Python production foundations, LangGraph agents, and FastAPI microservices.")
        print("="*60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lookup.py <company_or_role_name>")
    else:
        lookup_company(" ".join(sys.argv[1:]))
