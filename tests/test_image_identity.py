import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'ZCU216/packages/release-identity/sanitize.py'
spec = importlib.util.spec_from_file_location('sanitize', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ImageIdentityTests(unittest.TestCase):
    def fixture(self, root):
        for name in ('etc/ssh', 'var/lib/dbus', 'var/lib/systemd', 'home/xilinx/.ssh', 'root'):
            (root / name).mkdir(parents=True, exist_ok=True)
        for name, text in {'etc/os-release': 'NAME=PynqLinux\n', 'etc/hosts': '127.0.0.1 localhost\n127.0.1.1 pynq\n', 'etc/machine-id': 'shared-id', 'etc/ssh/ssh_host_ed25519_key': 'shared-private', 'home/xilinx/.ssh/authorized_keys': 'personal-key', 'root/.bash_history': 'private-command', 'var/lib/systemd/random-seed': 'shared-seed', 'home/xilinx/keep.txt': 'application-data'}.items():
            (root / name).write_text(text)

    def test_identity_removed_and_unrelated_data_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            module.sanitize(root)
            module.sanitize(root)  # idempotent offline preparation
            self.assertEqual((root / 'etc/machine-id').read_bytes(), b'')
            self.assertEqual((root / 'var/lib/dbus/machine-id').readlink(), Path('/etc/machine-id'))
            self.assertFalse((root / 'etc/ssh/ssh_host_ed25519_key').exists())
            self.assertFalse((root / 'home/xilinx/.ssh/authorized_keys').exists())
            self.assertFalse((root / 'root/.bash_history').exists())
            self.assertFalse((root / 'var/lib/systemd/random-seed').exists())
            self.assertEqual((root / 'etc/hostname').read_text(), 'pynq-zcu216\n')
            self.assertEqual((root / 'home/xilinx/keep.txt').read_text(), 'application-data')

    def test_refuses_host_root(self):
        with self.assertRaises(ValueError):
            module.sanitize('/')

    def test_refuses_escaping_symlink_without_touching_target(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as external:
            root = Path(directory)
            self.fixture(root)
            (root / 'etc/hosts').unlink()
            outside = Path(external) / 'hosts'
            outside.write_text('outside')
            (root / 'etc/hosts').symlink_to(outside)
            with self.assertRaises(ValueError):
                module.sanitize(root)
            self.assertEqual(outside.read_text(), 'outside')
