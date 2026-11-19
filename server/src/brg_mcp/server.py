"""The BRG MCP server.

Every markdown file ``src/brg_mcp/<folder>/<page>.md`` (or ``<folder>/<subfolder>/<page>.md``) is one command.
``readme.md`` is the command of the folder, every other page adds its name::

    fd/readme.md                     ->   fd
    fd/01_algorithm.md               ->   fd_algorithm
    fd/10_compas/03_hypar_membrane.md ->  fd_compas_hypar_membrane
    tna/06_compas/09_barrel_vault.md  ->  tna_compas_barrel_vault

A new command is a new markdown file; this file does not change.
Each command reaches the chatbot in two ways:

* through the tool ``command``: the user types ``mcp_brg_fd`` and the model calls the tool with it,
* as a prompt, which some chatbots show as a slash command (Claude Code: ``/mcp__brg__fd``).

``uv run brg-mcp`` runs the server. It waits for a chatbot on stdin and stdout; it is not a chat.

"""

import re
from pathlib import Path

from fastmcp import FastMCP

from brg_mcp.teaching import link
from brg_mcp.teaching import notebooks_of
from brg_mcp.teaching import plain
from brg_mcp.teaching import title

HERE = Path(__file__).parent


# ==============================================================================
# Commands
# ==============================================================================


def command_name(path):
    """Name the command of a markdown file.

    Parameters
    ----------
    path : :class:`pathlib.Path`
        A markdown file inside ``src/brg_mcp/``.

    Returns
    -------
    str
        ``<folder>`` for ``readme.md``, ``<folder>_<page>`` (or ``<folder>_<subfolder>_<page>``) otherwise.

    """
    parts = [plain(part) for part in path.relative_to(HERE).with_suffix("").parts if part != "readme"]
    return "_".join(parts)


def _sort_key(path):
    rel = path.relative_to(HERE)
    return (rel.parts[0], len(rel.parts), path.stem != "readme", rel.parts)


# Finds the file names.
COMMANDS = {command_name(path): path for path in sorted([*HERE.glob("*/*.md"), *HERE.glob("*/*/*.md")], key=_sort_key)}


def summary(path):
    """Return a short one-line label from the first line of ``path``."""
    first = path.read_text(encoding="utf-8").strip().splitlines()[0].lstrip("# ").rstrip(":")
    if len(first) > 90:
        return "Overview"
    return first.split(":", 1)[0].strip()


def command_list():
    """Format the menu: one line per method, with its package.

    A method is a folder with a ``readme.md``, such as ``fd/``. Its package is the folder ``compas_<method>/``, such as ``compas_fd/``.
    The pages of a method are listed by the method's own command, ``mcp_brg_fd``, not here.

    Returns
    -------
    str

    """
    folders = sorted(path.parent.name for name, path in COMMANDS.items() if path.stem == "readme" and path.parent.parent == HERE)
    lines = []
    for folder in folders:
        if folder.startswith("compas_") and folder.removeprefix("compas_") in folders:
            continue
        line = "- `mcp_brg_{}`: {}".format(folder, summary(COMMANDS[folder]))
        if "compas_" + folder in folders:
            line += ", package `compas_{0}` (`mcp_brg_compas_{0}`)".format(folder)
        lines.append(line)
    return (
        "Reply with this exact Markdown list (keeping headings, bullet points, and code formatting intact), "
        "then ask which method the user wants:\n\n## BRG methods\n\n" + "\n".join(lines)
    )


# A page with Python code shows the script (with compas_viewer) and offers to save and run it.
RUN = (
    "Reply with the full Markdown text below (keeping all headings, bullet lists, links, and the complete Python code block with `compas_viewer` intact). "
    "At the end, ask the user if they want you to save and run the Python script now. "
    "When the user confirms, write the Python code block to its named `.py` file in the current working folder, "
    "exactly as shown: do not add docstrings, comments or any other text, "
    "ensure {names} are installed (if no active Python environment has them, install `uv` if missing, "
    "run `uv init --bare` and `uv add {packages}`), and run `uv run python <file>.py` so it prints the output "
    "and opens the 3D `compas_viewer` window.\n\n"
)


def packages_of(text):
    """The COMPAS packages that the Python code of a page imports, besides ``compas`` itself.

    Parameters
    ----------
    text : str
        The text of a page with a Python code block.

    Returns
    -------
    list[str]
        For example ``["compas_tna", "compas_viewer"]``, the viewer last.

    """
    packages = set(re.findall(r"^(?:from|import) (compas_[a-z]+)", text, re.M))
    return sorted(packages, key=lambda package: (package == "compas_viewer", package))


def reply(name):
    """The text of a command, formatted for chat display.

    The ``readme.md`` of a folder ends with the list of the other pages in that folder, in the order of their numbers.
    A page with a notebook folder of the same name, numbers aside, such as ``06_exercises.md`` and ``07_exercises/``, ends with a link
    to each notebook in it, which opens the notebook in the Jupyter of the teaching website.

    Parameters
    ----------
    name : str
        A key of ``COMMANDS``.

    Returns
    -------
    str

    """
    path = COMMANDS[name]
    text = path.read_text(encoding="utf-8").strip()
    if path.stem == "readme":
        pages = [other for other in COMMANDS if other != name and COMMANDS[other].parent == path.parent]
        text += "\n\n## More information\n\n" + "\n".join(
            "- {}: `mcp_brg_{}`".format(page.removeprefix(name + "_").capitalize(), page) for page in pages
        )
    notebooks = notebooks_of(path)
    if notebooks:
        text += "\n\n## Notebooks\n\n" + "\n".join("- [{}]({})".format(title(notebook), link(notebook)) for notebook in notebooks)
    if "```python" in text:
        packages = packages_of(text)
        return RUN.format(names=" and ".join("`{}`".format(package) for package in packages), packages=" ".join(packages)) + text.strip()
    return "Reply with this exact Markdown text (keeping all headings, bullet lists, and links intact), nothing added:\n\n" + text.strip()


# ==============================================================================
# Server
# ==============================================================================

RULE = (
    "When the user's message is mcp_brg or mcp_brg_<name>, with or without a leading /, "
    "call the tool `command` of this server with the message as `name` and do what the result says. "
    "mcp_brg lists the commands: {}."
).format(", ".join("mcp_brg_{}".format(name) for name in COMMANDS))

mcp = FastMCP("brg", instructions=RULE)


def add_prompt(name):
    """Offer a command as a prompt, which chatbots show as a slash command.

    Parameters
    ----------
    name : str
        A key of ``COMMANDS``.

    """
    mcp.prompt(name=name, description="BRG {}".format(name))(lambda: reply(name))


for name in COMMANDS:
    add_prompt(name)


@mcp.tool(
    description=RULE,
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
def command(name: str):
    """Answer a command typed as text, for chatbots without slash commands.

    Parameters
    ----------
    name : str
        The command, for example ``mcp_brg_fd``, ``/mcp_brg_fd`` or ``fd``.
        The type hint stays: MCP reads it to tell the chatbot that ``name`` is text.

    Returns
    -------
    str

    """
    name = name.strip().lstrip("/").removeprefix("mcp__brg__").removeprefix("mcp_brg").lstrip("_")
    if name not in COMMANDS:
        return command_list()
    return reply(name)


# ==============================================================================
# FastMCP
# ==============================================================================


@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run()
