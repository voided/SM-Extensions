import tempfile
import unittest
import tarfile
import zipfile
from pathlib import Path

from release_packages import assemble


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.artifacts = self.root / 'artifacts'
        self.output = self.root / 'assets'
        self.project = 'SourceScramble'
        self.version = '0.8.2.2'
        self.arches = ['x86', 'x86_64']
        self.platforms = ['linux', 'windows']
        for sm in ('1.12', '1.13'):
            for platform in self.platforms:
                for arch in self.arches:
                    package = self.package(sm, platform, arch)
                    ext = package / 'extensions'
                    if arch == 'x86_64':
                        ext /= 'x64'
                    ext.mkdir(parents=True)
                    (ext / ('sourcescramble.ext.' + ('so' if platform == 'linux' else 'dll'))).write_bytes(arch.encode())
                    for relative in ('scripting/include/sourcescramble.inc', 'plugins/sourcescramble_manager.smx'):
                        file = package / relative
                        file.parent.mkdir(parents=True, exist_ok=True)
                        file.write_bytes(sm.encode())

    def package(self, sm, platform, arch):
        return self.artifacts / f'pkg-{self.project}-{self.version}-sm{sm}-{platform}-{arch}' / 'addons/sourcemod'

    def assemble(self):
        assemble(self.project, self.version, self.arches, self.platforms, self.artifacts, self.output)

    def test_platform_archives_contain_both_architectures(self):
        self.assemble()
        self.assertEqual(len(list(self.output.iterdir())), 4)
        for archive in self.output.iterdir():
            if archive.suffix == '.zip':
                with zipfile.ZipFile(archive) as file:
                    files = set(file.namelist())
                suffix = 'dll'
            else:
                with tarfile.open(archive) as file:
                    files = set(file.getnames())
                suffix = 'so'
            self.assertIn(f'addons/sourcemod/extensions/sourcescramble.ext.{suffix}', files)
            self.assertIn(f'addons/sourcemod/extensions/x64/sourcescramble.ext.{suffix}', files)
            self.assertIn('addons/sourcemod/plugins/sourcescramble_manager.smx', files)

    def test_x86_only_archives(self):
        self.arches = ['x86']
        self.assemble()
        for archive in self.output.glob('*.zip'):
            with zipfile.ZipFile(archive) as file:
                self.assertIn('addons/sourcemod/extensions/sourcescramble.ext.dll', file.namelist())
                self.assertNotIn('addons/sourcemod/extensions/x64/sourcescramble.ext.dll', file.namelist())

    def test_missing_binary_fails_release(self):
        (self.package('1.12', 'linux', 'x86') / 'extensions/sourcescramble.ext.so').unlink()
        with self.assertRaises(FileNotFoundError):
            self.assemble()

    def test_conflicting_common_file_fails_release(self):
        (self.package('1.12', 'linux', 'x86_64') / 'scripting/include/sourcescramble.inc').write_bytes(b'different')
        with self.assertRaises(ValueError):
            self.assemble()


if __name__ == '__main__':
    unittest.main()
