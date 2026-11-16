#!/usr/bin/env python3
"""Reset only generated identity/authentication state in an offline image root."""
import argparse
from pathlib import Path
import re


def sanitize(root):
    root = Path(root).resolve()
    if root == Path('/') or not (root / 'etc/os-release').is_file():
        raise ValueError('Expected an offline image root containing etc/os-release')

    for relative in ('etc', 'etc/ssh', 'etc/hosts', 'root', 'home/xilinx', 'var/lib/dbus', 'var/lib/dhcp', 'var/lib/NetworkManager'):
        if not (root / relative).resolve().is_relative_to(root):
            raise ValueError(f'Path escapes offline root: {relative}')

    def remove(relative):
        path = root / relative
        # Resolve the parent, never follow a final symlink out of the image.
        if not path.parent.resolve().is_relative_to(root):
            raise ValueError(f'Parent escapes offline root: {relative}')
        if path.is_symlink() or path.is_file():
            path.unlink()

    for path in (root / 'etc/ssh').glob('ssh_host_*'):
        remove(path.relative_to(root))
    for home in ('root', 'home/xilinx'):
        for name in ('.bash_history', '.python_history', '.lesshst', '.ssh/authorized_keys', '.ssh/id_rsa', '.ssh/id_ed25519', '.ssh/id_ecdsa'):
            remove(f'{home}/{name}')
    for relative in ('etc/machine-id', 'var/lib/dbus/machine-id', 'var/lib/systemd/random-seed'):
        remove(relative)
    (root / 'etc/machine-id').write_text('')
    (root / 'var/lib/dbus').mkdir(parents=True, exist_ok=True)
    (root / 'var/lib/dbus/machine-id').symlink_to('/etc/machine-id')
    for directory in ('var/lib/dhcp', 'var/lib/NetworkManager'):
        for path in (root / directory).glob('*lease*'):
            remove(path.relative_to(root))
    (root / 'etc/hostname').write_text('pynq-zcu216\n')
    hosts = root / 'etc/hosts'
    text = hosts.read_text()
    text = re.sub(r'^127\.0\.1\.1\s+.*$', '127.0.1.1\tpynq-zcu216', text, flags=re.M)
    if not re.search(r'^127\.0\.1\.1\s', text, re.M):
        text += '\n127.0.1.1\tpynq-zcu216\n'
    hosts.write_text(text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root')
    sanitize(parser.parse_args().root)
