import subprocess
import json
import time

def inspect_linkedin():
    js = """
    (() => {
        const cards = Array.from(document.querySelectorAll('.jobs-search-results__list-item, .job-card-container, [data-occludable-job-id]'));
        const titles = cards.map(c => {
            const titleEl = c.querySelector('.job-card-list__title, .artdeco-entity-lockup__title');
            const compEl = c.querySelector('.job-card-container__primary-description, .artdeco-entity-lockup__subtitle');
            const hasEasy = c.innerText.includes('Easy Apply');
            return {
                title: titleEl ? titleEl.innerText.trim() : '',
                comp: compEl ? compEl.innerText.trim() : '',
                hasEasy
            };
        });
        const easyApplyBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Easy Apply'));
        return {
            title: document.title,
            cardCount: cards.length,
            sample: titles.slice(0, 8),
            easyApplyButtonsOnPage: easyApplyBtns.length
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437702", js], capture_output=True, text=True)
    print("LINKEDIN JOBS:", res.stdout)

if __name__ == "__main__":
    inspect_linkedin()
