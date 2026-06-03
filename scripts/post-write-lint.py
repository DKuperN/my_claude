"""
PostToolUse Write hook — runs npm lint when a TS/JS file is written.
Called by Claude Code with tool context on stdin (JSON).
"""
import sys
import json
import subprocess
import pathlib

try:
    data = json.load(sys.stdin)
    fp = data.get('tool_input', {}).get('file_path', '')

    if not fp:
        sys.exit(0)

    if not any(fp.endswith(e) for e in ['.ts', '.tsx', '.js', '.jsx']):
        sys.exit(0)

    # Walk up to find nearest package.json
    d = pathlib.Path(fp).resolve().parent
    for _ in range(7):
        if (d / 'package.json').exists():
            r = subprocess.run(
                ['npm', 'run', 'lint', '--if-present'],
                cwd=str(d),
                capture_output=True,
                text=True,
                timeout=30
            )
            if r.returncode != 0:
                print('[LINT FAIL] Fix before committing:')
                print((r.stdout + r.stderr).strip()[-600:])
            break
        parent = d.parent
        if parent == d:
            break
        d = parent

except Exception:
    pass
