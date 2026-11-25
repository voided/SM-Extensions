#!/usr/bin/env python3
"""Merge x86/x64 install trees and produce one archive per SM version and OS."""
import argparse
import filecmp
import shutil
import tarfile
import zipfile
from pathlib import Path

from build_extension import PROJECTS, verify


def merge(source, destination):
    for path in sorted((source / 'addons').rglob('*')):
        target = destination / path.relative_to(source)
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                if not filecmp.cmp(path, target, shallow=False):
                    raise ValueError(f'Conflicting package files: {path} and {target}')
            else:
                shutil.copy2(path, target)


def assemble(project, version, architectures, platforms, artifacts, output):
    output.mkdir(parents=True, exist_ok=True)
    for sm in ('1.12', '1.13'):
        for platform in platforms:
            name = f'{project}-{version}-sm{sm}-{platform}'
            package = output.parent / 'packages' / name
            package.mkdir(parents=True, exist_ok=False)
            for arch in architectures:
                source = artifacts / f'pkg-{name}-{arch}'
                verify(project, source, arch, platform)
                merge(source, package)
            for arch in architectures:
                verify(project, package, arch, platform)
            if platform == 'linux':
                with tarfile.open(output / (name + '.tar.gz'), 'w:gz') as archive:
                    archive.add(package / 'addons', arcname='addons')
            else:
                with zipfile.ZipFile(output / (name + '.zip'), 'w', zipfile.ZIP_DEFLATED) as archive:
                    for file in sorted((package / 'addons').rglob('*')):
                        if file.is_file():
                            archive.write(file, file.relative_to(package))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('project', choices=PROJECTS)
    parser.add_argument('version')
    parser.add_argument('--architectures', nargs='+', required=True, choices=('x86', 'x86_64'))
    parser.add_argument('--platforms', nargs='+', required=True, choices=('windows', 'linux'))
    parser.add_argument('--artifacts', type=Path, default=Path('artifacts'))
    parser.add_argument('--output', type=Path, default=Path('assets'))
    args = parser.parse_args()
    assemble(args.project, args.version, args.architectures, args.platforms, args.artifacts, args.output)


if __name__ == '__main__':
    main()
