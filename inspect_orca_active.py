import subprocess
import json

def inspect_active():
    js = """
    (() => {
        const text = document.body.innerText;
        const dialog = document.querySelector('[role="dialog"], .modal-content, .drawer, [class*="modal"]');
        const textareas = Array.from(document.querySelectorAll('textarea')).map(t => ({ placeholder: t.placeholder, value: t.value }));
        const btns = Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
        return {
            hasDialog: !!dialog,
            dialogText: dialog ? dialog.innerText.slice(0, 400) : null,
            textareas,
            buttons: btns.slice(0, 10),
            snippet: text.slice(0, 400)
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437656", js], capture_output=True, text=True)
    print("ORCA TAB STATE:", res.stdout)

if __name__ == "__main__":
    inspect_active()
