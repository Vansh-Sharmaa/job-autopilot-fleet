import subprocess
import json

def inspect_cards():
    js = """
    (() => {
        const items = Array.from(document.querySelectorAll('.jobs-search-results__list-item, [data-occludable-job-id]'));
        return items.map((it, idx) => {
            const title = it.querySelector('.job-card-list__title, [class*="job-title"]')?.innerText?.trim();
            const comp = it.querySelector('.job-card-container__primary-description, [class*="company-name"]')?.innerText?.trim();
            const hasEasy = it.innerText.includes('Easy Apply');
            return { idx, title, comp, hasEasy };
        });
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437702", js], capture_output=True, text=True)
    print("CARDS:", res.stdout)

if __name__ == "__main__":
    inspect_cards()
