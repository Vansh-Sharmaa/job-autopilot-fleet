import subprocess
import json

def inspect_main():
    js = """
    (() => {
        const text = document.body.innerText;
        const main = document.querySelector('main');
        const lists = Array.from(document.querySelectorAll('ul')).map(ul => ({
            class: ul.className,
            childrenCount: ul.children.length,
            sampleText: ul.innerText.slice(0, 150)
        }));
        return {
            title: document.title,
            listsCount: lists.length,
            lists: lists.slice(0, 10)
        };
    })()
    """
    res = subprocess.run(["browse", "eval", "--tab", "12437702", js], capture_output=True, text=True)
    print("MAIN:", res.stdout)

if __name__ == "__main__":
    inspect_main()
