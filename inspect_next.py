import subprocess
import json

def inspect_next():
    js = """
    (() => {
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
        if (!nextBtn) return { hasNext: false };
        let parent = nextBtn;
        for (let i = 0; i < 6; i++) {
            if (!parent.parentElement) break;
            parent = parent.parentElement;
        }
        return {
            hasNext: true,
            containerTag: parent.tagName,
            containerClass: parent.className,
            containerText: parent.innerText.slice(0, 500),
            inputs: Array.from(parent.querySelectorAll('input, select, textarea')).map(i => ({
                tag: i.tagName,
                type: i.type,
                value: i.value,
                placeholder: i.placeholder
            }))
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437702", js], capture_output=True, text=True)
    print("NEXT CONTAINER:", res.stdout)

if __name__ == "__main__":
    inspect_next()
