import asyncio
import re
import sys
from pathlib import Path

import pytest
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

from brg_mcp.server import COMMANDS
from brg_mcp.server import mcp
from brg_mcp.server import reply
from brg_mcp.teaching import link
from brg_mcp.teaching import notebooks_of


def ask(question):
    """Start the server the way a chatbot does and ask it ``question(client)``."""

    async def run():
        transport = StdioTransport(command=str(Path(sys.executable).parent / "brg-mcp"), args=[], keep_alive=False)
        async with Client(transport) as client:
            return await question(client)

    return asyncio.run(asyncio.wait_for(run(), timeout=20))


def test_instructions_name_every_command():
    assert all("mcp_brg_{}".format(name) in mcp.instructions for name in COMMANDS)


def test_readme_lists_the_pages_of_its_folder():
    text = ask(lambda client: client.call_tool("command", {"name": "mcp_brg_fd"})).content[0].text
    assert all("mcp_brg_{}".format(name) in text for name in COMMANDS if COMMANDS[name].parent.name == "fd" and name != "fd")
    compas_text = ask(lambda client: client.call_tool("command", {"name": "mcp_brg_fd_compas"})).content[0].text
    assert all("mcp_brg_{}".format(name) in compas_text for name in COMMANDS if name.startswith("fd_compas_"))


def test_tna_lists_its_pages_and_examples():
    text = ask(lambda client: client.call_tool("command", {"name": "mcp_brg_tna"})).content[0].text
    assert all("mcp_brg_{}".format(name) in text for name in COMMANDS if COMMANDS[name].parent.name == "tna" and name != "tna")
    examples = [name for name in COMMANDS if name.startswith("tna_compas_")]
    compas_text = ask(lambda client: client.call_tool("command", {"name": "mcp_brg_tna_compas"})).content[0].text
    assert len(examples) == 10 and all("mcp_brg_{}".format(name) in compas_text for name in examples)


@pytest.mark.parametrize("name", ["fd_exercises", "fd_extensions"])
def test_page_lists_the_notebooks_of_its_folder(name):
    text = ask(lambda client: client.call_tool("command", {"name": name})).content[0].text
    notebooks = notebooks_of(COMMANDS[name])
    assert notebooks and all(link(notebook) in text for notebook in notebooks)


def test_server_offers_every_command():
    prompts = ask(lambda client: client.list_prompts())
    tools = ask(lambda client: client.list_tools())
    assert {prompt.name for prompt in prompts} == set(COMMANDS)
    assert "fd" in COMMANDS
    assert {tool.name for tool in tools} == {"command", "greet"}


@pytest.mark.parametrize("typed", ["mcp_brg_fd", "/mcp_brg_fd", "fd", "/mcp__brg__fd"])
def test_prompt_and_tool_reply_the_same(typed):
    prompt = ask(lambda client: client.get_prompt("fd"))
    tool = ask(lambda client: client.call_tool("command", {"name": typed}))
    assert prompt.messages[0].content.text == tool.content[0].text


@pytest.mark.parametrize("typed", ["mcp_brg", "/mcp_brg", "nothing"])
def test_mcp_brg_lists_the_methods_and_their_packages(typed):
    tool = ask(lambda client: client.call_tool("command", {"name": typed}))
    text = tool.content[0].text
    assert "- `mcp_brg_fd`: Force density method, package `compas_fd` (`mcp_brg_compas_fd`)" in text
    assert "- `mcp_brg_tna`: Thrust network analysis, package `compas_tna` (`mcp_brg_compas_tna`)" in text
    assert "mcp_brg_fd_algorithm" not in text


def test_every_command_is_reachable_from_the_menu():
    menu = ask(lambda client: client.call_tool("command", {"name": "mcp_brg"})).content[0].text
    seen, todo = set(), re.findall(r"mcp_brg_([a-z_]+)", menu)
    while todo:
        name = todo.pop()
        if name not in seen:
            seen.add(name)
            todo += re.findall(r"mcp_brg_([a-z_]+)", reply(name))
    assert seen == set(COMMANDS)


@pytest.mark.parametrize("name", sorted(COMMANDS))
def test_every_command_named_in_a_text_exists(name):
    for named in re.findall(r"mcp_brg_([a-z_]+)", COMMANDS[name].read_text(encoding="utf-8")):
        assert named in COMMANDS


@pytest.mark.parametrize("name", [cmd for cmd in sorted(COMMANDS) if "```python" in COMMANDS[cmd].read_text(encoding="utf-8")])
def test_python_examples_include_viewer_and_offer_to_run(name):
    text = reply(name)
    assert "from compas_viewer import Viewer" in text
    assert "viewer.show()" in text
    assert "save and run the Python script" in text
    package = "compas_tna" if name.startswith("tna") else "compas_fd"
    assert "uv add {} compas_viewer".format(package) in text
