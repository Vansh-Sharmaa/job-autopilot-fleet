import subprocess
import json

def inspect_hyrezy():
    js = """
    (() => {
        const allEls = Array.from(document.querySelectorAll('*')).filter(el => el.innerText && el.innerText.includes('HYrEzy'));
        if (allEls.length === 0) return { status: 'not found' };
        const deepest = allEls[allEls.length - 1];
        return {
            tag: deepest.tagName,
            class: deepest.className,
            text: deepest.innerText,
            parentTag: deepest.parentElement?.tagName,
            parentClass: deepest.parentElement?.className,
            grandParentTag: deepest.parentElement?.parentElement?.tagName
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437702", js], capture_output=True, text=True)
    print("HYREZY ELEMENT:", res.stdout)

if __name__ == "__main__":
    inspect_hyrezy()
