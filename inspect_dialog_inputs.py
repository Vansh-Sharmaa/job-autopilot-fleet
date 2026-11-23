import subprocess
import json

def inspect_dialog_inputs():
    js = """
    (() => {
        const dialog = document.querySelector('[role="dialog"], .modal-content, .drawer, [class*="modal"]');
        if (!dialog) return { hasDialog: false };
        const inputs = Array.from(dialog.querySelectorAll('input, select, textarea')).map(i => ({
            tag: i.tagName,
            type: i.type,
            name: i.name,
            id: i.id,
            placeholder: i.placeholder,
            value: i.value,
            className: i.className
        }));
        const buttons = Array.from(dialog.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            disabled: b.disabled,
            className: b.className
        }));
        return {
            hasDialog: true,
            inputs,
            buttons
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437656", js], capture_output=True, text=True)
    print("DIALOG INPUTS:", res.stdout)

if __name__ == "__main__":
    inspect_dialog_inputs()
