#!/usr/bin/env bash
set -eo pipefail
source /etc/profile.d/pynq_venv.sh
python3 - <<'PY'
import importlib.metadata as metadata
import json
from pathlib import Path
import subprocess
import sys
pins = json.loads(Path('/usr/local/share/zcu216-build-inputs.json').read_text())['python_git_dependencies']
distributions = {'PYNQ-Metadata': 'pynqmetadata', 'PYNQ-Utils': 'pynqutils'}
for repository, revision in pins.items():
    def installed_commit():
        info = metadata.distribution(distributions[repository]).read_text('direct_url.json')
        return json.loads(info or '{}').get('vcs_info', {}).get('commit_id')
    if installed_commit() != revision:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--force-reinstall', '--no-deps', f'git+https://github.com/Xilinx/{repository}.git@{revision}'])
    assert installed_commit() == revision, (repository, installed_commit(), revision)
    print('Verified installed dependency:', repository, revision, flush=True)
PY
