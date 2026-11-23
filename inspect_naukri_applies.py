import subprocess
import json
import time

def inspect():
    js = """
    (() => {
        const text = document.body.innerText;
        return {
            title: document.title,
            snippet: text.slice(text.indexOf('Applies ('), text.indexOf('Applies (') + 1000)
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437597", js], capture_output=True, text=True)
    print("OUTPUT:", res.stdout)

if __name__ == "__main__":
    inspect()
