# brg_framework

Shared knowledge for the Block Research Group Python packages: theory, teaching material, and links to the packages. Installing Python and COMPAS itself is covered by [COMPAS](https://compas.dev). This repository adds BRG theory and pointers to the individual BRG packages.

## Layout of this repository

```text
brg_framework/
├── AGENTS.md                  # for people and agents editing this repository
├── theory/
│   ├── fd/                    # force density
│   │   ├── index.md           # what, when, assumptions, limits
│   │   ├── formulation.md     # equations with stable ids
│   │   ├── glossary.md
│   │   ├── references.md
│   │   └── teaching/          # exercises, notebooks, slides
│   └── tna/ ...
├── catalog/
│   ├── packages.toml          # package names, repositories, docs
│   └── methods.md             # method to package table
├── skills/
│   └── brg-methods/SKILL.md   # which method, which package, where it is
├── server/                    # the MCP server (FastMCP)
├── evals/                     # tasks, checkers, runner
└── README.md                  # installation
```

## The rules

- **Links.** This repository does not describe how to use each package. It only says which package to use and where it is.
    - The `brg-methods` skill picks the package and gives its repository and docs.
    - If the package ships its own skill or `AGENTS.md`, the agent follows it.
    - If not, the agent reads the package itself: README, docs, examples, tests and the docstrings of the installed version.
    - What a package ships is up to its developers.
- **One source.** Knowledge is Markdown files to be available to chatbots.
- **The installed package is the API truth.** The agent checks the installed version and reads its docstrings.
- **One MCP server.** For learners it returns the full BRG text.
- **Skills follow the [Agent Skills specification](https://agentskills.io/specification).** The `name` is lowercase with hyphens and equals the folder name. The `description` says what it does and when to use it.
- **Every example in this repository is a real `.py` file that CI runs** against a pinned package version.


## What belongs where

| Content | Home |
| --- | --- |
| Method theory: derivations, assumptions, limits, glossary, papers | `brg_framework` |
| Teaching: exercises, notebooks, slides | `brg_framework` |
| Catalog: package names, repositories, docs | `brg_framework` |
| Method-choice skill | `brg_framework` |
| MCP server | `brg_framework`, in `server/` |
| Everything about one package: code, docs, examples, tests, its own skill if any | the package |

No package imports `brg_framework`. It is content, not a runtime dependency.

## Users

| Who | How they get it | Folder |
| --- | --- | --- |
| Coders | The `brg-methods` skill, which points to the right package | `skills/` |
| Students | Hosted MCP server, each student adds it once to their own account | `server/` |
| Everyone else | Website | [brg.ethz.ch](https://brg.ethz.ch/) |

| | Learners | Coders |
| --- | --- | --- |
| Who | Students and others who want to read theory, see examples and do exercises. They do not write a project | People writing Python with BRG packages |
| What they ask | "Explain force density." "Show me a hypar example." "Give me exercise 2." | "Form-find this net with compas_fd." "Why does my solver fail?" |
| Door | The MCP server | The `brg-methods` skill, then the package |
| Why | Nothing to install. Always the newest text. The full answer appears in the chat, not a link | Works with the installed package version. The agent reads only what it needs |
| Extras | Links to notebooks on the teaching website | Optional hooks that copy examples as files |

## Installation Users - MCP

#### Claude

- Click your name (bottom left) → Settings → Connectors. On some versions it's the left menu → Plugins.
- Click Add → Add custom connector.
- Name: BRG. URL: **https://brg-mcp.fastmcp.app/mcp**. Leave the OAuth fields empty, then click Add.
- Start a new chat and type mcp_brg.
- You should see the "BRG methods" menu.


## Installation Devs - Skills


#### Claude
```bash
npx skills add petrasvestartas/brg_framework -g -y -a claude-code
```

#### Codex
```bash
npx skills add petrasvestartas/brg_framework -g
```







## MCP server

- Lives in `server/` in this repository, built with FastMCP.
- Hosted at one web address. Each student adds it to their own account.
- Reads the same Markdown files. It holds no content of its own.
- Returns the full text, and the chat shows it as the answer.
- No per-package servers.

## Scripts and hooks

Goal: copy code as it is, without the model retyping it. A script that copies a file costs almost no tokens and no waiting.

Two layers, one script:

1. **Script in the skill (works everywhere).** `skills/brg-methods/scripts/copy_example.py` copies an example file from a package into the project. The skill text tells the agent to run it. Scripts are part of the Agent Skills standard, so this works in all four agent apps with no setup.
2. **Hook (optional, faster).** The agent app runs the same script by itself at a fixed moment, without a model call.

Rules that keep hooks compatible with all four agent apps:

- **One script does the work**: `hooks/brg_hook.py`. No logic lives in a config file.
- **Only the four shared events**: `SessionStart`, `PreToolUse`, `PostToolUse`, `Stop`.
- **The script reads JSON from stdin and accepts both spellings** of each field (`tool_name` and `toolName`), because the agent apps differ.
- **Four small config files call that one script.** `brg hooks install` writes them.
- **Nothing depends on a hook.** Everything a hook does must also be reachable through the skill script.

| Agent app | Hook config written by the installer |
| --- | --- |
| Claude Code | `.claude/settings.json` |
| Codex | `.codex/hooks.json` (the user must review and trust it once) |
| Antigravity | `.agents/hooks.json` |
| Kimi Code | `[[hooks]]` in the user's `~/.kimi-code/config.toml`; it has no project-level hook file |

```text
brg_framework/
├── hooks/
│   ├── brg_hook.py            # the one script
│   └── install.py             # writes the four config files
└── skills/brg-methods/
    └── scripts/copy_example.py
```

## Measure first

Compare setups on the same tasks: package only, the server, the skill, the skill and the server. Record input, cached and output tokens, model calls, wall time, and pass or fail. Judge correctness first, then tokens, then time. No saving is claimed until these numbers exist.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [AGENTS.md](https://agents.md/)
- [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [FastMCP](https://gofastmcp.com/docs/changelog)
- [AAIF projects](https://aaif.io/projects)
