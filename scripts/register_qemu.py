#!/usr/bin/env python3
"""Register the container's AArch64 interpreter for privileged image chroots."""
from pathlib import Path
import subprocess

root=Path('/proc/sys/fs/binfmt_misc')
if not (root/'register').exists():
    subprocess.run(['mount','-t','binfmt_misc','binfmt_misc',str(root)],check=True)
entry=root/'qemu-aarch64-pynq'
if not entry.exists():
    magic=r'\x7f\x45\x4c\x46\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\xb7\x00'
    mask=r'\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff'
    (root/'register').write_text(f':qemu-aarch64-pynq:M::{magic}:{mask}:/usr/bin/qemu-aarch64-static:F')
text=entry.read_text()
assert text.startswith('enabled\n'), 'PYNQ AArch64 binfmt entry is disabled'
assert 'interpreter /usr/bin/qemu-aarch64-static\n' in text, 'Unexpected existing PYNQ interpreter'
assert any(line.startswith('flags:') and 'F' in line.split(':',1)[1] for line in text.splitlines()), 'PYNQ AArch64 binfmt entry needs flag F for chroots'
print('PYNQ AArch64 binfmt ready with flag F')
