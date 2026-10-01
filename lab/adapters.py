"""Send one prompt to one model through the official tool the user is logged into.

Every adapter returns a dict:
    {"text", "error", "model_reported", "usage", "seconds"}

Nothing here reads, copies or stores any login token: the official, unmodified CLIs
(Claude Code, Codex, Antigravity) handle authentication themselves.
Each call runs in an empty working folder with tools off (Claude), a read-only sandbox and
an isolated profile (Codex), or Antigravity's default agent setup (no system-prompt option).
"""
import json
import os
import shutil
import subprocess
import time

LAB = os.path.dirname(os.path.abspath(__file__))
# The CLIs show the model its working directory. The original folder (".../AI Lying Video/lab/workdir") told
# the Claude models what the test was for, and Opus mentioned it in 43 of 177 answers. Runs from 30 Sep 2026
# evening use a neutral folder (override with LAB_WORKDIR).
WORK = os.environ.get("LAB_WORKDIR", r"E:\scratch\session")
os.makedirs(WORK, exist_ok=True)
NEUTRAL_SYSTEM = "You are a helpful assistant."
CODEX_HOME = os.path.join(LAB, "codex_home")
APPDATA = os.environ.get("APPDATA", "")
LOCALAPPDATA = os.environ.get("LOCALAPPDATA", "")


def _exe(path, fallback):
    return path if os.path.exists(path) else (shutil.which(fallback) or fallback)


CLAUDE = _exe(os.path.join(APPDATA, "npm", "node_modules", "@anthropic-ai", "claude-code", "bin", "claude.exe"), "claude")
CODEX = _exe(os.path.join(APPDATA, "npm", "node_modules", "@openai", "codex", "node_modules", "@openai",
                          "codex-win32-x64", "vendor", "x86_64-pc-windows-msvc", "bin", "codex.exe"), "codex")
AGY = _exe(os.path.join(LOCALAPPDATA, "agy", "bin", "agy.exe"), "agy")


# Prompts go to the CLIs as a command-line argument, and Windows caps a whole command line at 32,767 characters
# (WinError 206 beyond that). Quoting can add up to ~20% (every " becomes \"), so batched grader prompts stay well below.
MAX_PROMPT_CHARS = 22000


def batches(keys, line, most):
    """Split keys into batches of at most `most` whose rendered lines (line(key)) fit MAX_PROMPT_CHARS together."""
    out, cur, size = [], [], 0
    for k in keys:
        n = len(line(k)) + 1
        if cur and (len(cur) >= most or size + n > MAX_PROMPT_CHARS):
            out.append(cur)
            cur, size = [], 0
        cur.append(k)
        size += n
    return out + ([cur] if cur else [])


def _run(cmd, env=None, timeout=900):
    t0 = time.time()
    try:
        r = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout, env=env, cwd=WORK)
        return r, time.time() - t0, None
    except subprocess.TimeoutExpired:
        return None, time.time() - t0, f"timeout after {timeout}s"


def _result(text=None, error=None, model_reported=None, usage=None, seconds=0.0):
    return {"text": text, "error": error, "model_reported": model_reported, "usage": usage,
            "seconds": round(seconds, 1)}


def claude(model, prompt, system=NEUTRAL_SYSTEM):
    cmd = [CLAUDE, "-p", prompt, "--model", model, "--system-prompt", system, "--tools", "",
           "--setting-sources", "", "--no-session-persistence", "--output-format", "json",
           "--strict-mcp-config"]   # no MCP servers: without this the account's claude.ai connectors (Gmail,
                                    # Calendar, Drive) load into the context, and Opus mentioned them in 9/40 answers
    r, secs, err = _run(cmd)
    if err:
        return _result(error=err, seconds=secs)
    try:
        d = json.loads(r.stdout)
    except ValueError:
        return _result(error=f"unparseable (exit {r.returncode}): {r.stdout[:200]} {r.stderr[:200]}", seconds=secs)
    if d.get("is_error"):
        return _result(error=str(d.get("result"))[:300], seconds=secs)
    return _result(d.get("result"), None, ",".join((d.get("modelUsage") or {}).keys()), d.get("usage"), secs)


def codex(model, prompt, system_file=None, effort=None):
    env = dict(os.environ, CODEX_HOME=CODEX_HOME)
    cmd = [CODEX, "exec", "--sandbox", "read-only", "--ephemeral", "--skip-git-repo-check", "--json",
           "-C", WORK, "-m", model]
    if system_file:
        cmd += ["-c", f'model_instructions_file="{system_file}"']
    if effort:
        cmd += ["-c", f'model_reasoning_effort="{effort}"']
    cmd.append(prompt)
    r, secs, err = _run(cmd, env=env)
    if err:
        return _result(error=err, seconds=secs)
    text, usage, errors = None, None, []
    for line in r.stdout.splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        item = e.get("item") or {}
        if item.get("type") == "agent_message":
            text = item.get("text")
        elif e.get("type") == "turn.completed":
            usage = e.get("usage")
        elif e.get("type") in ("error", "turn.failed"):
            errors.append(json.dumps(e)[:300])
    if text is None:
        tail = [l for l in r.stderr.splitlines() if "error" in l.lower()][-2:]
        return _result(error=("; ".join(errors) or " | ".join(tail) or f"no answer (exit {r.returncode})")[:400],
                       seconds=secs)
    return _result(text, None, model, usage, secs)


def agy(model, prompt):
    cmd = [AGY, "-p", prompt, "--model", model, "--output-format", "json"]
    r, secs, err = _run(cmd)
    if err:
        return _result(error=err, seconds=secs)
    try:
        d = json.loads(r.stdout)
    except ValueError:
        return _result(error=f"unparseable (exit {r.returncode}): {r.stdout[:200]} {r.stderr[:200]}", seconds=secs)
    text = d.get("response")
    if not text or str(d.get("status", "")).lower() not in ("", "success", "completed", "ok"):
        return _result(text, f"status={d.get('status')}", model, d.get("usage"), secs)
    return _result(text, None, model, d.get("usage"), secs)


def _env_value(name):
    """Read one value from lab/.env (created by the user). Never printed or logged."""
    path = os.path.join(LAB, ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8-sig", errors="replace"):
            line = line.strip()
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'") or None
    return os.environ.get(name) or None


DEEPSEEK_BASE = "https://api.deepseek.com"


def _deepseek_request(path, body=None, timeout=600):
    import urllib.error
    import urllib.request
    key = _env_value("DEEPSEEK_API_KEY")
    if not key:
        raise RuntimeError("DEEPSEEK_API_KEY missing from lab/.env")
    req = urllib.request.Request(DEEPSEEK_BASE + path,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}") from None


def deepseek(model, prompt, system=NEUTRAL_SYSTEM):
    t0 = time.time()
    try:
        d = _deepseek_request("/chat/completions", {
            "model": model, "stream": False,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]})
    except Exception as e:                                   # noqa: BLE001 - logged as a row error
        return _result(error=str(e)[:400], seconds=time.time() - t0)
    choice = (d.get("choices") or [{}])[0].get("message") or {}
    return _result(choice.get("content"), None, d.get("model"), d.get("usage"), time.time() - t0)


PROVIDERS = {"claude": claude, "codex": codex, "agy": agy, "deepseek": deepseek}
