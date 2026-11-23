import subprocess
import json
import time

def test_foundit_children():
    url = "https://www.foundit.in/srp/results?query=Python+Developer&experienceRanges=0~2&quickApplyJobs=true"
    nav = subprocess.run(["browse", "navigate", url], capture_output=True, text=True)
    tab_id = json.loads(nav.stdout).get("tab")
    time.sleep(5)
    
    js = """
    (() => {
        const container = document.querySelector('.srpResultCard');
        if (!container) return { status: 'no container' };
        const children = Array.from(container.children).map(c => ({
            tag: c.tagName,
            class: c.className,
            textSnippet: c.innerText.slice(0, 100)
        }));
        return {
            containerClass: container.className,
            children
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", str(tab_id), js], capture_output=True, text=True)
    print("CHILDREN:", res.stdout)
    subprocess.run(["browse", "tabs", "--tab", str(tab_id), "close"], capture_output=True)

if __name__ == "__main__":
    test_foundit_children()
