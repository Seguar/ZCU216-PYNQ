import hashlib
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class PortTests(unittest.TestCase):
    def test_current_port_contract(self):
        spec=importlib.util.spec_from_file_location('port_check',ROOT/'scripts/check_port.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        module.check(ROOT)

    def test_archived_binary_bytes_match_original_commit(self):
        for name in ('base.bit','base.hwh','base.xsa'):
            original=subprocess.check_output(['git','-C',str(ROOT),'show','60be175:ZCU216/'+name])
            self.assertEqual(hashlib.sha256(original).digest(),hashlib.sha256((ROOT/'legacy/overlays/base'/name).read_bytes()).digest())

    def test_packaged_defaults_match_board_tables(self):
        source=ROOT/'ZCU216/tics'
        packaged=ROOT/'ZCU216/packages/tics/tics'
        self.assertEqual({p.name for p in source.glob('*.txt')},{p.name for p in packaged.glob('*.txt')})
        for path in source.glob('*.txt'):
            self.assertEqual(path.read_bytes(),(packaged/path.name).read_bytes())

    def test_recovered_runtime_clock_manifest_unchanged(self):
        original=subprocess.check_output(['git','-C',str(ROOT),'show','60be175:runtime/beamforming/clocks/manifest.json'])
        self.assertEqual(original,(ROOT/'runtime/beamforming/clocks/manifest.json').read_bytes())

if __name__=='__main__': unittest.main()
