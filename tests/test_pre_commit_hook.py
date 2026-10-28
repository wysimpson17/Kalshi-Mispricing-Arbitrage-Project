import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
# Split so the hook doesn't block committing this file.
KEY = "-----BEGIN RSA PRIVATE KEY" + "-----\nMIIfake\n"


def git(cwd, *args):
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t.invalid", "-c", "commit.gpgsign=false", *args],
        cwd=cwd, capture_output=True, text=True,
    )


def test_hook_blocks_private_keys_and_allows_normal_commits(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "core.hooksPath", str(REPO / ".githooks"))
    (tmp_path / "notes.md").write_text("hi\n")
    git(tmp_path, "add", "notes.md")
    assert git(tmp_path, "commit", "-qm", "normal").returncode == 0

    # utf-16 is what Windows PowerShell's > writes; git sees it as binary.
    for name, encoding in [("my-bot.txt", "ascii"), ("pasted.txt", "utf-16")]:
        (tmp_path / name).write_text(KEY, encoding=encoding)
        git(tmp_path, "add", name)
        assert "Commit blocked" in git(tmp_path, "commit", "-qm", "key").stderr, name
        git(tmp_path, "rm", "-q", "--cached", name)


def test_hook_is_turned_on_in_this_clone():
    # Git never turns hooks on by itself: if this fails, run the setup steps in README.md.
    assert git(REPO, "config", "core.hooksPath").stdout.strip() == ".githooks"
