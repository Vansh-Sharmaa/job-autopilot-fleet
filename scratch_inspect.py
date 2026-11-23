import subprocess
import json
import time

def run():
    # close tab 12433161
    subprocess.run(["browse", "tabs", "--tab", "12433161", "close"], capture_output=True)
    
    # navigate to hirist
    res = subprocess.run(["browse", "navigate", "https://www.hirist.tech/jobfeed?minexp=0&maxexp=2"], capture_output=True, text=True)
    print("NAV:", res.stdout)
    data = json.loads(res.stdout)
    tab_id = data.get("tab")
    time.sleep(4)
    
    js = """
    (() => {
        const jobs = Array.from(document.querySelectorAll('.job-card, .jobFeedCard, .feed-card, [data-job-id], .job-tuple'));
        return {
            title: document.title,
            jobsCount: jobs.length,
            snippet: document.body.innerText.slice(0, 500)
        };
    })()
    """
    res2 = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("EVAL:", res2.stdout)
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    run()
