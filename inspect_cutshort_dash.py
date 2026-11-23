import subprocess
import json

def inspect_dashboard():
    js = """
    (() => {
        const links = Array.from(document.querySelectorAll('a')).map(a => ({ text: a.innerText.trim(), href: a.href }));
        const viewJobs = links.filter(l => l.text.toLowerCase().includes('job') || l.href.includes('job'));
        return {
            title: document.title,
            jobLinks: viewJobs
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437653", js], capture_output=True, text=True)
    print("DASHBOARD LINKS:", res.stdout)
    subprocess.run(["browse", "tabs", "--tab", "12437653", "close"], capture_output=True)

if __name__ == "__main__":
    inspect_dashboard()
