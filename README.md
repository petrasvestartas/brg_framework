# brg_framework

Shared knowledge for the Block Research Group Python packages. Installing Python and COMPAS itself is covered by [COMPAS](https://compas.dev). This repository adds BRG theory and pointers to the individual BRG packages.

## Layout of this repository

```text
brg_framework/
├── AGENTS.md                      # for people and agents editing this repository
├── README.md                      # this file
├── theory/                        # one folder per method: fd, dr, tna, tno, dem, ags
│   └── fd/
│       ├── index.md               # what, when, assumptions, limits
│       ├── formulation.md         # equations with stable ids
│       ├── glossary.md
│       ├── references.md
│       └── teaching/              # exercises, notebooks, slides
├── catalog/
│   ├── packages.toml              # package names, repositories, docs
│   └── methods.md                 # method to package table
├── skills/
│   └── brg-methods/
│       ├── SKILL.md               # which method, which package, where it is
│       └── scripts/
│           └── copy_example.py    # copies a BRG example as a .py file
├── server/                        # the MCP server (FastMCP)
│   ├── INSTALL.md                 # add the server to each app
│   ├── pyproject.toml
│   ├── src/brg_mcp/
│   │   ├── server.py              # every .md page below is one command
│   │   ├── teaching.py            # brg-publish: notebooks to the teaching website
│   │   ├── fd/                    # force density pages and examples
│   │   ├── tna/                   # thrust network analysis pages and examples
│   │   ├── compas_fd/
│   │   └── compas_tna/
│   └── tests/
└── evals/                         # tasks and results, still empty
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

## Users

| | Learners `skills/` | Coders `server/` |
| --- | --- | --- |
| Who | Students and others who want to read theory, see examples and do exercises. They do not write a project | People writing Python with BRG packages |
| What they ask | "Explain force density." "Show me a hypar example." "Give me exercise 2." | "Form-find this net with compas_fd." "Why does my solver fail?" |
| Door | The MCP server | The `brg-methods` skill, then the package |
| Why | Nothing to install. Always the newest text. The full answer appears in the chat, not a link | Works with the installed package version. The agent reads only what it needs |
| Extras | Links to notebooks on the teaching website | A script that copies examples as files |

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

**Script (works now).** `skills/brg-methods/scripts/copy_example.py` copies a BRG example into the current folder. Only the Python standard library. It installs with the skill, and the skill tells the agent to run it.

```bash
python copy_example.py                    # list the examples
python copy_example.py tna_cross_vault    # write tna_cross_vault.py
```

**Hooks (planned, not built).** The agent app would run the same script by itself, without a model call. Build them only if the measurements below show they save something.

## Measure first

Compare setups on the same tasks: package only, the server, the skill, the skill and the server. Record input, cached and output tokens, model calls, wall time, and pass or fail. Judge correctness first, then tokens, then time. No saving is claimed until these numbers exist.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [AGENTS.md](https://agents.md/)
- [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [FastMCP](https://gofastmcp.com/docs/changelog)
- [AAIF projects](https://aaif.io/projects)
