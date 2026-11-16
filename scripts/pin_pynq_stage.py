#!/usr/bin/env python3
"""Render the pinned upstream PYNQ stage without changing its other behavior."""
import json
from pathlib import Path
import re
import sys

repo = Path(__file__).resolve().parents[1]
pins = json.loads((repo / 'docs/build-inputs.json').read_text())['python_git_dependencies']
text = Path(sys.argv[1]).read_text()
for name, revision in pins.items():
    if not re.fullmatch('[0-9a-f]{40}', revision):
        raise ValueError(f'Unpinned dependency: {name}')
    original = f'git+https://github.com/Xilinx/{name}.git\n'
    if text.count(original) != 1:
        raise ValueError(f'Unexpected upstream PYNQ stage: {name}')
    text = text.replace('python3 -m pip install --upgrade ' + original, 'python3 -m pip install --upgrade --force-reinstall --no-deps ' + original.rstrip('\n') + '@' + revision + '\n')
sys.stdout.write(text)
