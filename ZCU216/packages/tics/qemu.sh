#!/usr/bin/env bash
# SPDX-License-Identifier: BSD-3-Clause
set -eo pipefail
source /etc/profile.d/pynq_venv.sh
python3 - <<'TICS'
import importlib.util
import shutil
from pathlib import Path
spec = importlib.util.find_spec('xrfclk')
if spec is None or not spec.submodule_search_locations:
    raise RuntimeError('Install xrfclk before the board clock tables')
destination = Path(next(iter(spec.submodule_search_locations)))
files = sorted(Path('/usr/local/share/zcu216-tics').glob('*.txt'))
if not files:
    raise RuntimeError('Missing ZCU216 clock tables')
for source in files:
    shutil.copy2(source, destination/source.name)
print('Installed', len(files), 'clock tables without programming hardware')
TICS
