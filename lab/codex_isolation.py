"""Build the per-run `-c` overrides that isolate a `codex exec` call from Maiko's personal
Codex setup (AGENTS.md notes, memories, plugins/MCP tools, web search, shell tool).

Nothing here writes to ~/.codex: config.toml is only READ (to list plugin names), and every
override is passed on the command line for that single run. auth.json is never opened.
"""
import os
import re

LAB = os.path.dirname(os.path.abspath(__file__))
NEUTRAL = os.path.join(LAB, "neutral_instructions.md").replace("\\", "/")
CONFIG = os.path.join(os.path.expanduser("~"), ".codex", "config.toml")


def codex_exe():
    """The official native codex.exe that the npm `codex.cmd` wrapper launches (called directly
    so Python passes arguments without cmd.exe re-quoting them)."""
    base = os.path.join(os.environ.get("APPDATA", ""), "npm", "node_modules", "@openai", "codex",
                        "node_modules", "@openai", "codex-win32-x64", "vendor", "x86_64-pc-windows-msvc",
                        "bin", "codex.exe")
    return base if os.path.exists(base) else "codex"


def plugin_names():
    names = []
    try:
        for line in open(CONFIG, encoding="utf-8", errors="replace"):
            m = re.match(r'^\s*\[plugins\."([^"]+)"\]\s*$', line)   # top-level plugin tables only
            if m:
                names.append(m.group(1))
    except FileNotFoundError:
        pass
    return names


def overrides(instructions_file=NEUTRAL):
    flags = [
        f'model_instructions_file="{instructions_file}"',
        "project_doc_max_bytes=0",
        "memories.use_memories=false",
        "memories.generate_memories=false",
        'web_search="disabled"',
        "features.shell_tool=false",
    ]
    flags += [f'plugins."{name}".enabled=false' for name in plugin_names()]
    args = []
    for f in flags:
        args += ["-c", f]
    return args


if __name__ == "__main__":
    print(len(plugin_names()), "plugins found; override args:", len(overrides()) // 2)
