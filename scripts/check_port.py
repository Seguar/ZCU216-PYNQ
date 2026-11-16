#!/usr/bin/env python3
"""Hardware-free port validation; does not configure RF clocks or program an FPGA."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def check(root=ROOT):
    inputs=json.loads((root/'docs/build-inputs.json').read_text())
    actual=subprocess.check_output(['git','-C',str(root/'PYNQ'),'rev-parse','HEAD'],text=True).strip()
    assert actual==inputs['pynq_commit'], 'PYNQ submodule is not the pinned current release'
    env={}
    for line in (root/'ZCU216/edf.env').read_text().splitlines():
        if line.strip() and not line.lstrip().startswith('#'):
            k,v=line.split('=',1);env[k]=v.strip('"')
    assert env['EDF_MODE']=='custom'
    assert env['EDF_BOOT_MACHINE']==inputs['custom_machine']
    assert env['EDF_BOARD_DTS']==inputs['sdt_board']
    assert env['EDF_MANIFEST_TAG']==inputs['edf_manifest_tag']
    cells=[int(x,0) for x in env['EDF_DDR_HIGH_BANK_REG'].split()]
    assert cells==[8,0,0,0x80000000] and inputs['ps_ddr_bytes']==4*1024**3
    assert (root/'ZCU216/hardware/export.tcl').is_file()
    assert not list((root/'ZCU216').rglob('*.bit')), 'Historical bitstreams must not enter current overlay discovery'
    legacy=json.loads((root/'docs/legacy-artifacts.json').read_text())
    for name,expected in legacy['files'].items():
        assert hashlib.sha256((root/'legacy/overlays/base'/name).read_bytes()).hexdigest()==expected
    clocks=json.loads((root/'runtime/beamforming/clocks/manifest.json').read_text())
    for item in clocks['files']:
        assert hashlib.sha256((root/'runtime/beamforming/clocks'/item['file']).read_bytes()).hexdigest()==item['sha256']
    manifest=json.loads((root/'ZCU216/selftest.json').read_text())
    for item in manifest['tests']:
        for key in ('python','bash'):
            if item['id'].startswith(key+'/'):
                suffix='.py' if key=='python' else '.sh'
                test=root/'PYNQ/sdbuild/packages/selftest/tests'/(item['id']+suffix)
                assert test.is_file(), 'Unknown upstream self-test: '+item['id']
        assert item.get('hardware',False) is False
    assert manifest['defaults']['hardware'] is False
    print('PASS: pinned EDF port, stock DDR limit, legacy isolation, preserved clocks, valid non-RF self-tests')

if __name__=='__main__':check()
