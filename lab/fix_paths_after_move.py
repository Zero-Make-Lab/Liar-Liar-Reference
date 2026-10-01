"""One-off: rewrite absolute Downloads paths to their new home on E:\\Video Ideas after the move.
Text files only; skips virtualenvs, caches and Codex's internal state (except its config.toml)."""
import os

ROOT = r"E:\Video Ideas"
TEXT_EXT = {".md", ".py", ".bat", ".toml", ".json", ".csv", ".txt"}
SKIP_DIRS = {".venv", "cache", "workdir", "B-roll", "Images", "Newspapers", "Document-pages", "Previews",
             "plugins", "log", "tmp", "skills", "__pycache__", "pylib"}
OLD_NEW = []
for name, new_parent in [("Computers Were Built With Cables", ROOT), ("AI Lying Video", ROOT), ("AI Water Video", ROOT),
                         ("Rope Model Image Prompt", ROOT + r"\Computers Were Built With Cables")]:
    old_bs = r"C:\Users\maiko\Downloads" + "\\" + name
    new_bs = new_parent + "\\" + name
    OLD_NEW += [(old_bs, new_bs),                                                     # C:\Users\...
                (old_bs.replace("\\", "/"), new_bs.replace("\\", "/")),              # C:/Users/...
                (old_bs.replace("\\", "\\\\"), new_bs.replace("\\", "\\\\"))]        # JSON-escaped
# build_rope_model.py builds its output folder with os.path.join(... "Downloads", ...)
OLD_NEW.append(('OUT_DIR = os.path.join(os.path.expanduser("~"), "Downloads",\n'
                '                       "Computers Were Built With Cables", "3D-model")',
                'OUT_DIR = r"E:\\Video Ideas\\Computers Were Built With Cables\\3D-model"'))

changed = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    in_codex_home = "codex_home" in dirpath.split(os.sep)
    for fn in filenames:
        if os.path.splitext(fn)[1].lower() not in TEXT_EXT or fn == os.path.basename(__file__):
            continue
        if in_codex_home and fn != "config.toml":
            continue
        path = os.path.join(dirpath, fn)
        try:
            raw = open(path, "rb").read()
            text = raw.decode("utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new = text
        for old, rep in OLD_NEW:
            new = new.replace(old, rep)
            if "\r\n" in text:                       # CRLF files: match multi-line patterns too
                new = new.replace(old.replace("\n", "\r\n"), rep)
        if new != text:
            open(path, "wb").write(new.encode("utf-8"))
            changed.append(os.path.relpath(path, ROOT))
print(f"{len(changed)} files updated:")
for c in changed:
    print("  ", c)
