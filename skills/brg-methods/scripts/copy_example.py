"""Copy a BRG example script into the current folder, without retyping it.

    python copy_example.py                     list the examples
    python copy_example.py tna_cross_vault     write tna_cross_vault.py here

The examples are the pages ``server/src/brg_mcp/<method>/<nn>_compas/<nn>_<name>.md`` of the BRG framework on GitHub.
Only the Python standard library is used. Set ``BRG_REPO`` to read another fork, for example ``BlockResearchGroup/brg_framework``.

"""

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

REPO = os.environ.get("BRG_REPO", "petrasvestartas/brg_framework")
BRANCH = os.environ.get("BRG_BRANCH", "main")
PAGE = re.compile(r"^server/src/brg_mcp/([a-z]+)/\d+_compas/\d+_([a-z0-9_]+)\.md$")
CODE = re.compile(r"```python\n(.*?)```", re.DOTALL)


def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": "brg-copy-example"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def name_of(path):
    """``server/src/brg_mcp/tna/06_compas/10_cross_vault.md`` -> ``tna_cross_vault``, or None for other files."""
    match = PAGE.match(path)
    return "{}_{}".format(*match.groups()) if match else None


def code_of(text):
    """The first Python code block of a page."""
    match = CODE.search(text)
    if not match:
        raise ValueError("the page has no Python code block")
    return match.group(1)


def examples():
    """Every example name and the path of its page."""
    tree = json.loads(get("https://api.github.com/repos/{}/git/trees/{}?recursive=1".format(REPO, BRANCH)))["tree"]
    return {name_of(item["path"]): item["path"] for item in tree if name_of(item["path"])}


def main(args):
    pages = examples()
    if not args:
        print("\n".join(sorted(pages)))
        return 0
    name = args[0].removesuffix(".py")
    if name not in pages:
        print("No example {}. Run without a name to list them.".format(name), file=sys.stderr)
        return 1
    target = Path("{}.py".format(name))
    if target.exists() and "--force" not in args:
        print("{} exists. Add --force to overwrite it.".format(target), file=sys.stderr)
        return 1
    text = get("https://raw.githubusercontent.com/{}/{}/{}".format(REPO, BRANCH, pages[name]))
    target.write_text(code_of(text), encoding="utf-8")
    print("wrote {}".format(target.resolve()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
