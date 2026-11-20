"""The command ``brg``.

brg install                 copy the brg-methods skill into Claude Code and the other agents, print the MCP address
brg examples                list the BRG examples
brg copy tna_cross_vault    write tna_cross_vault.py into the current folder
brg version                 the versions of brg_framework and the BRG packages

"""

import argparse
import importlib.metadata
import importlib.util
import shutil
import sys
from pathlib import Path

from brg_framework import MCP_URL
from brg_framework import PACKAGES
from brg_framework import __version__

HERE = Path(__file__).parent
SKILL = "brg-methods"

# Claude Code reads ~/.claude/skills. Codex, Antigravity, Kimi Code and others read ~/.agents/skills.
AGENT_FOLDERS = [Path(".claude") / "skills", Path(".agents") / "skills"]


def skill_folder():
    """The skill shipped in the package, or the one in the repository for an editable install."""
    for folder in (HERE / "skills" / SKILL, HERE.parents[1] / "skills" / SKILL):
        if (folder / "SKILL.md").exists():
            return folder
    raise FileNotFoundError("the {} skill is missing from this installation".format(SKILL))


def copy_example():
    """The script of the skill that copies examples. It is written once, in the skill."""
    path = skill_folder() / "scripts" / "copy_example.py"
    spec = importlib.util.spec_from_file_location("brg_copy_example", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def install(home):
    """Copy the skill into every agent folder under ``home``. Return the folders written."""
    source = skill_folder()
    written = []
    for folder in AGENT_FOLDERS:
        target = home / folder / SKILL
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__"))
        written.append(target)
    return written


def versions():
    lines = ["brg_framework {}".format(__version__)]
    for name in PACKAGES:
        try:
            lines.append("{} {}".format(name, importlib.metadata.version(name)))
        except importlib.metadata.PackageNotFoundError:
            lines.append("{} not installed".format(name))
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(prog="brg", description="Block Research Group: skill, MCP server and examples for coding agents.")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("install", help="copy the skill into Claude Code and the other agents, print the MCP address")
    commands.add_parser("examples", help="list the BRG examples")
    copy = commands.add_parser("copy", help="write an example as a .py file into the current folder")
    copy.add_argument("name", help="for example tna_cross_vault")
    copy.add_argument("--force", action="store_true", help="overwrite the file if it exists")
    commands.add_parser("version", help="the versions of brg_framework and the BRG packages")
    args = parser.parse_args(argv)

    if args.command == "install":
        for target in install(Path.home()):
            print("skill: {}".format(target))
        print("MCP server: {}".format(MCP_URL))
        print("Add it to your app once: https://github.com/BlockResearchGroup/brg_framework/blob/main/server/INSTALL.md")
        return 0
    if args.command == "examples":
        return copy_example().main([])
    if args.command == "copy":
        return copy_example().main([args.name] + (["--force"] if args.force else []))
    if args.command == "version":
        print("\n".join(versions()))
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
