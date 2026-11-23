import subprocess
import json

def inspect_page_after_click():
    js = """
    (() => {
        const text = document.body.innerText;
        // Search for keywords like "Contact info", "Next", "Submit application", "Resume"
        const buttons = Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
        const hasContactInfo = text.includes('Contact info');
        const hasResume = text.includes('Resume');
        return {
            hasContactInfo,
            hasResume,
            buttons: buttons.slice(0, 20),
            tailSnippet: text.slice(text.length - 800)
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437702", js], capture_output=True, text=True)
    print("PAGE STATE:", res.stdout)

if __name__ == "__main__":
    inspect_page_after_click()
