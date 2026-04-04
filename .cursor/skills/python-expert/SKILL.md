---
name: python-expert
description: Python edge cases, clever tricks, and finicky OS issues. Use when working with Python scripts, cross-platform behavior, encoding, path handling, subprocess, Windows vs Linux, or when Python code behaves unexpectedly.
---

# Python Expert

Apply when the task involves Python development, debugging unexpected behavior, cross-platform scripts, or OS-specific issues. Focus on edge cases and gotchas the agent might not handle correctly by default.

## Edge Cases and Gotchas

### Mutable Default Arguments

```python
# BAD - same list reused across calls
def append_to(items=[]):
    items.append(1)
    return items

# GOOD
def append_to(items=None):
    if items is None:
        items = []
    items.append(1)
    return items
```

Same applies to dicts, sets, any mutable. Never use mutable defaults.

### Float Precision and Comparisons

- Avoid `==` for floats. Use `math.isclose(a, b)` or `abs(a - b) < epsilon`.
- `0.1 + 0.2 == 0.3` is False. Decimal for money/financial.

### Truthiness Surprises

- `bool([])`, `bool({})`, `bool(0)`, `bool(0.0)` all False.
- `bool("")` False; `bool(" ")` True.
- `bool([0])` True (non-empty list).
- `or`/`and` return the last evaluated value, not necessarily bool: `[] or "default"` → `"default"`.

### `is` vs `==`

- `is` checks identity (same object); `==` checks equality.
- Small integers (-5..256) are interned: `a = 256; b = 256; a is b` may be True.
- Use `is None`, `is not None`. Never `== None` for singletons.
- For other objects, prefer `==`.

### Iteration and Modification

- Don't modify a list/dict while iterating over it. Use a copy or iterate in reverse for list removal.
- `for k in list(d.keys())` when mutating `d`.

### Encoding and Text

- **Open files:** Prefer `encoding="utf-8"` explicitly. Use `errors="replace"` or `errors="ignore"` for dirty input.
- **Windows:** Console/stdout may be cp1252 or cp437. Scripts writing to pipe/file: set `PYTHONIOENCODING=utf-8` or `sys.stdout.reconfigure(encoding="utf-8")` (3.7+).
- **BOM:** `encoding="utf-8-sig"` when reading CSV/Excel from Windows.

### Path Handling (OS Finicky)

- Use `pathlib.Path` over string concatenation. `Path("a") / "b"` works on Windows and Unix.
- Never hardcode `\` or `/`. `Path` handles separators.
- `Path.cwd()` vs `os.getcwd()`—Path is cleaner.
- **Windows:** `Path` normalizes mixed slashes. Long paths: enable long path support or use `\\\\?\\` prefix for very long paths.
- **Paths as strings:** Use `str(path)` when an API expects a string (e.g. `open()`, subprocess).

### Subprocess and Shell

- Prefer `subprocess.run(..., capture_output=True, text=True)` over `os.system` or `shell=True`.
- **Windows:** `shell=True` often needed to run `.bat`/`.cmd` or commands that rely on `cmd` (e.g. `dir`). For `.exe` directly, `shell=False` is safer.
- **Windows:** `CreateProcess` fails if executable path has spaces and isn't quoted. Use list form: `subprocess.run(["program", "arg1"], ...)`.
- **Line endings:** `subprocess` returns `\n`; Windows native is `\r\n`. Normalize if comparing.

### Environment and Working Directory

- `os.environ` is process-local. Changes in script don't persist to parent shell (by design).
- `Path.cwd()` can change with `os.chdir()`. Capture at start if you need the original.

## Clever Tricks (Use Sparingly)

### `pathlib` one-liners

```python
list(Path(".").rglob("*.py"))   # All .py files recursively
Path("a/b/c").relative_to("a") # Path("b/c")
```

### `itertools` for iteration

- `itertools.islice` for lazy slicing of iterators.
- `itertools.groupby` requires sorted input; use `operator.itemgetter` or lambda for key.
- `more_itertools.chunked` for batching (or `zip(*[iter(it)]*n)`).

### Context managers for temp state

```python
with contextlib.redirect_stdout(open(os.devnull, 'w')):
    noisy_function()
```

### Walrus operator (`:=`)

- `if (m := re.match(pat, s)):` to both match and capture.

## Windows-Specific Issues

### Path length

- Legacy 260-char limit. Use `pathlib` and avoid deep nesting; or enable long paths in policy/registry.

### Line endings

- Files: `"wb"` for binary; `"w"` uses `\n` unless `newline` is set. Use `newline=""` for CSV to avoid double-translation.

### `subprocess` and `PATH`

- `shutil.which("cmd")` to find executable. On Windows, `PATH` may include extensions; `subprocess` will add `.exe` when `shell=False`.

### PowerShell vs cmd

- Scripts assuming bash (e.g. `&&`, `|`) fail in cmd. Document "run in PowerShell" or use cross-platform logic.

## Quick Reference

| Issue | Recommendation |
|-------|----------------|
| Paths | `pathlib.Path`, never raw `\` |
| Encoding | `encoding="utf-8"`, `errors="replace"` for dirty input |
| Mutable defaults | Use `None` and assign inside |
| Float equality | `math.isclose` or epsilon |
| None check | `is None` / `is not None` |
| Modify while iterate | Iterate copy or `list(d.keys())` |
| Subprocess | List args, avoid `shell=True` when possible |
| Windows spaces in path | Use list form for `subprocess` |
