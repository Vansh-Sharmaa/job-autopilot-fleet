import subprocess
import json

def confirm_discard():
    js = """
    (() => {
        const discardBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim().toLowerCase() === 'discard');
        if (discardBtn) {
            discardBtn.click();
            return { discarded: true };
        }
        return { discarded: false };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437702", js], capture_output=True, text=True)
    print("DISCARD RES:", res.stdout)

if __name__ == "__main__":
    confirm_discard()
