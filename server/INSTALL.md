# Install the BRG MCP server

The server runs online. You add one address to your app. Nothing to install.

```text
https://brg-mcp.fastmcp.app/mcp
```

Then type `mcp_brg` in a new chat. You see the list of BRG methods.

## Claude (web, desktop, phone)

1. Open claude.ai. Go to **Settings → Connectors**.
2. Click **Add custom connector**.
3. Name: `BRG`. URL: the address above. Leave OAuth empty.
4. Click **Add**.

Done once per account. It then works on every device, and in Claude Code too.

## Claude Code

Same Claude account as above: nothing to do. BRG shows up as `claude.ai BRG`.

Other account:

```bash
claude mcp add --transport http --scope user brg https://brg-mcp.fastmcp.app/mcp
```

## ChatGPT

1. Go to **Settings → Apps & Connectors → Advanced settings**. Turn on **Developer mode**.
2. Click **Create**. Name: `BRG`. URL: the address above. Authentication: none.
3. In a chat, pick BRG from the **+** menu.

## Codex

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.brg]
url = "https://brg-mcp.fastmcp.app/mcp"
```

## Antigravity

Add to `~/.gemini/antigravity/mcp_config.json`. Restart Antigravity.

```json
{ "mcpServers": { "brg": { "serverUrl": "https://brg-mcp.fastmcp.app/mcp" } } }
```

## Gemini CLI

```bash
gemini mcp add --transport http brg https://brg-mcp.fastmcp.app/mcp
```

## Cursor

Add to `~/.cursor/mcp.json`:

```json
{ "mcpServers": { "brg": { "url": "https://brg-mcp.fastmcp.app/mcp" } } }
```

## Kimi Code

```bash
kimi mcp add --transport http brg https://brg-mcp.fastmcp.app/mcp
```

## Run the examples

Some pages end with a Python script. Say "yes" and the agent saves and runs it.
For this, install [uv](https://docs.astral.sh/uv/) once:

```bash
# Linux and macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

The agent installs `compas_fd`, `compas_tna` and `compas_viewer` itself.

## From a local clone

For people who edit the pages. Changes show after a restart of the server.

```bash
claude mcp add --scope user brg -- uv --directory /path/to/brg_framework/server run brg-mcp
```

Other apps: command `uv`, arguments `--directory /path/to/brg_framework/server run brg-mcp`.

## Tested

Claude and Claude Code. The other apps follow their own docs. If one fails, open an issue.
