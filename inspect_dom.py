import subprocess
import json

def inspect_dom():
    js = """
    (() => {
        const links = Array.from(document.querySelectorAll('a[href*="/jobs/view/"]')).map(a => ({
            text: a.innerText.trim(),
            href: a.href.split('?')[0]
        }));
        return {
            totalJobLinks: links.length,
            uniqueLinks: Array.from(new Set(links.map(l => l.href))).slice(0, 10),
            samples: links.slice(0, 10)
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437702", js], capture_output=True, text=True)
    print("JOB LINKS:", res.stdout)

if __name__ == "__main__":
    inspect_dom()
