# Kalshi Mispricing Arbitrage

## Set up a PC (once)

Needs [uv](https://docs.astral.sh/uv/). If `uv --version` fails, install it with `winget install astral-sh.uv`. Then, in this folder:

```powershell
uv venv
uv pip install -r requirements.txt
git config core.hooksPath .githooks
uv run pytest
```

- `uv venv` makes `.venv` with the Python version in `.python-version`, downloading it if needed. VS Code uses `.venv` automatically.
- The `git config` line turns on a check that refuses any commit containing a private key. Git never turns it on by itself. Keep your Kalshi key file outside this folder anyway.
- `uv run pytest` should pass. If it fails, a step above was missed.

## After every pull

```powershell
uv pip install -r requirements.txt
```

This installs the exact versions listed in `constraints.txt`.

## Adding or upgrading a package

```powershell
uv pip install -U <package>
uv pip freeze --exclude pip | Set-Content -Encoding ascii constraints.txt
```

Add new packages to `requirements.txt` too. Use `Set-Content`, not `>`: Windows PowerShell's `>` writes UTF-16, which git can't diff.
