import subprocess
import json

def dismiss_modal():
    js = """
    (() => {
        const dismissBtn = Array.from(document.querySelectorAll('button')).find(b => {
            const label = b.getAttribute('aria-label') || '';
            const text = b.innerText.trim();
            return label.toLowerCase().includes('dismiss') || label.toLowerCase().includes('close') || text === 'Discard';
        });
        if (dismissBtn) {
            dismissBtn.click();
            return { clicked: true, label: dismissBtn.getAttribute('aria-label') };
        }
        return { clicked: false };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437702", js], capture_output=True, text=True)
    print("DISMISS CLICK:", res.stdout)

if __name__ == "__main__":
    dismiss_modal()
