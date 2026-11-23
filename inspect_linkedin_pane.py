import subprocess
import json

def inspect_pane():
    js = """
    (() => {
        const btn = document.querySelector('.jobs-apply-button, button[class*="jobs-apply-button"]');
        const title = document.querySelector('.job-details-jobs-unified-top-card__job-title, h1')?.innerText?.trim();
        const comp = document.querySelector('.job-details-jobs-unified-top-card__company-name, .jobs-unified-top-card__company-name, [class*="company-name"]')?.innerText?.trim();
        return {
            hasBtn: !!btn,
            btnText: btn ? btn.innerText.trim() : null,
            title,
            comp
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437702", js], capture_output=True, text=True)
    print("RIGHT PANE:", res.stdout)

if __name__ == "__main__":
    inspect_pane()
