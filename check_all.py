from pathlib import Path
import ast
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    failed = False
    for folder in sorted((ROOT / "projects").iterdir()):
        source = folder / "main.py"
        try:
            ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        except (OSError, SyntaxError) as exc:
            print(f"FAIL {folder.name}: {exc}")
            failed = True
            continue
        result = subprocess.run(
            [sys.executable, "main.py", "--smoke"],
            cwd=folder,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = (result.stdout + result.stderr).strip()
        if result.returncode:
            print(f"FAIL {folder.name}: {output}")
            failed = True
        elif "SMOKE_SKIPPED" in output:
            print(f"SKIP {folder.name}: {output}")
        else:
            print(f"PASS {folder.name}: {output}")
    print("Available smoke checks passed." if not failed else "Some checks failed.")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
