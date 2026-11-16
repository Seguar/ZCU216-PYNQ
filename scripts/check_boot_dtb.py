#!/usr/bin/env python3
"""Read final loose DTB selected by extlinux; fail on ZCU216 port mismatches."""
import json
from pathlib import Path
import subprocess
import sys

dtb = sys.argv[1]

def prop(node, name, kind='s'):
    result = subprocess.run(['fdtget', '-t', kind, dtb, node, name], text=True, capture_output=True)
    return result.stdout.strip() if result.returncode == 0 else None

def walk(node='/'):
    yield node
    children = subprocess.check_output(['fdtget', '-l', dtb, node], text=True).splitlines()
    for child in children:
        yield from walk(node.rstrip('/') + '/' + child)

nodes = list(walk())
model = prop('/', 'model')
assert model and 'ZCU216' in model, model
assert prop('/chosen', 'pynq_board') == 'ZCU216'
memories = {}
for node in nodes:
    if prop(node, 'device_type') == 'memory' and prop(node, 'status') != 'disabled':
        cells = [int(x, 16) for x in prop(node, 'reg', 'x').split()]
        assert len(cells) % 4 == 0, cells
        memories[node] = [[(cells[i]<<32) + cells[i+1], (cells[i+2]<<32) + cells[i+3]] for i in range(0, len(cells), 4)]
linux_memory_bytes = sum(size for ranges in memories.values() for _, size in ranges)
assert linux_memory_bytes in (4 * 1024**3, 4 * 1024**3 - 1024**2), memories
assert memories.get('/memory@800000000') == [[0x800000000, 0x80000000]], memories
stdout = prop('/chosen', 'stdout-path')
assert stdout, 'Missing console selection'
serial = stdout.split(':')[0]
if not serial.startswith('/'):
    serial = prop('/aliases', serial)
assert serial and prop(serial, 'status') in ('okay', 'ok', None), serial
for node in nodes:
    compatible = prop(node, 'compatible') or ''
    assert not ('xlnx,xps-intc' in compatible and prop(node, 'status') != 'disabled'), node
bridge = [n for n in nodes if prop(n, 'compatible') == 'nxp,sc18is602b']
assert len(bridge) == 1, bridge
for name in ('lmk@1', 'lmxdac@2', 'lmxadc@3'):
    assert bridge[0] + '/' + name in nodes, name
cma = [n for n in nodes if prop(n, 'linux,cma-default', 'x') is not None]
assert len(cma) == 1, cma
assert prop(cma[0], 'size', 'x') in ('0 20000000', '20000000'), prop(cma[0], 'size', 'x')
clock = prop('/__symbols__', 'pss_ref_clk')
assert clock and int(prop(clock, 'clock-frequency', 'x'), 16) == 33333333
phy_details = {n: {'reg': prop(n, 'reg', 'x'), 'compatible': prop(n, 'compatible')} for n in nodes if '/ethernet-phy@' in n}
report = {'status': 'PASS', 'model': model, 'board': 'ZCU216', 'memory_ranges': memories, 'linux_memory_bytes': linux_memory_bytes, 'physical_ps_ddr_bytes': 4 * 1024**3, 'stdout_path': stdout, 'uart_node': serial, 'bootargs': prop('/chosen', 'bootargs'), 'clk104_bridge': bridge[0], 'cma': cma[0], 'ps_reference_hz': 33333333, 'phy_nodes': phy_details, 'enabled_pl_intc': False, 'scope': 'offline final DTB inspection; no board boot claim'}
print(json.dumps(report, indent=2))
