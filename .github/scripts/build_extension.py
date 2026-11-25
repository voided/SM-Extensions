#!/usr/bin/env python3
"""Configure an extension with AMBuild 2.2 and verify its installable package."""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# The native-architecture build and package specifics live here, keeping workflow
# wrappers small while letting each project retain its own AMBuild configuration.
PROJECTS = {
    'Accelerator': dict(binary='accelerator.ext', version='product.version', deps=False,
                        files=['gamedata/accelerator.games.txt', 'extensions/accelerator.autoload',
                               'scripting/include/accelerator.inc']),
    'Connect': dict(binary='connect.ext.2.tf2', version='product.version', sdk='legacy', auto_version=True,
                    files=['gamedata/connect.games.txt', 'scripting/include/connect.inc']),
    'ConsoleCleaner': dict(binary='cleaner.ext.2.tf2', version='smsdk_config.h', sdk='manifest',
                           files=['configs/cleaner.cfg', 'extensions/cleaner.autoload']),
    'LoadSoundScript': dict(binary='loadsoundscript.ext.2.tf2', version='sdk/smsdk_config.h', sdk='manifest',
                            package='loadsoundscript', files=['scripting/include/loadsoundscript.inc']),
    'SMJansson': dict(binary='smjansson.ext', version='sdk/smsdk_config.h', deps=False,
                      files=['scripting/include/smjansson.inc']),
    'SourceScramble': dict(binary='sourcescramble.ext', version='smsdk_config.h', plugin=True,
                          files=['scripting/include/sourcescramble.inc', 'plugins/sourcescramble_manager.smx']),
    'TFEconDynamic': dict(binary='tf2econdynamic.ext.2.tf2', version='product.version', sdk='manifest', plugin=True,
                         files=['gamedata/tf2.econ_dynamic.txt', 'scripting/include/tf_econ_dynamic.inc',
                                'plugins/tf_econ_dynamic_compat.smx']),
    'TFMaxSpeedDetour': dict(binary='tf_calcmaxspeed.ext.2.tf2', version='smsdk_config.h', sdk='legacy',
                            files=['gamedata/tf2.calcmaxspeed.txt', 'scripting/include/tf_calcmaxspeed.inc',
                                   'extensions/tf_calcmaxspeed.autoload']),
    'TFMaxVoiceSpeakDelayUnlimiter': dict(binary='TFMaxVoiceSpeakDelayUnlimiter.ext.2.tf2', version='sdk/smsdk_config.h', sdk='legacy'),
    'VScript': dict(binary='vscript.ext.2.tf2', version='product.version', sdk='vscript', auto_version=True,
                    files=['scripting/include/vscript.inc', 'extensions/vscript.autoload']),
}
ROOT = Path(__file__).resolve().parents[2]


def version(project):
    file = ROOT / project / PROJECTS[project]['version']
    content = file.read_text(encoding='utf-8-sig')
    if file.name == 'product.version':
        base = content.strip()
    else:
        match = re.search(r'^#define\s+SMEXT_CONF_VERSION\s+"([^"]+)"', content, re.MULTILINE)
        if not match:
            raise ValueError(f'Cannot locate extension version in {file}')
        base = match.group(1)
    base = base.replace('/', '-')  # SMJansson's native version contains a slash.
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9.-]*', base):
        raise ValueError(f'Invalid release version: {base}')
    count = subprocess.check_output(['git', 'rev-list', '--count', 'HEAD'], cwd=ROOT, text=True).strip()
    return f'{base}.{count}'


def package_path(project, build):
    return build / PROJECTS[project].get('package', 'package')


def verify(project, package, arch, platform):
    meta = PROJECTS[project]
    sm = package / 'addons/sourcemod'
    extension_dir = sm / 'extensions'
    if arch == 'x86_64':
        extension_dir /= 'x64'
    binary = extension_dir / (meta['binary'] + ('.dll' if platform == 'windows' else '.so'))
    if not binary.is_file() or not binary.stat().st_size:
        raise FileNotFoundError(f'Missing or empty binary: {binary}')
    for file in meta.get('files', []):
        if not (sm / file).is_file():
            raise FileNotFoundError(f'Missing package file: {sm / file}')
    print(f'Verified {binary}')


def build(project, output, deps, arch):
    meta = PROJECTS[project]
    source = ROOT / project
    sm = deps / 'sourcemod'
    args = [sys.executable, str(source / 'configure.py'), '--sm-path', str(sm),
            '--enable-optimize', '--targets', arch]
    if meta.get('deps', True):
        args += ['--mms-path', str(deps / 'metamod-source')]
    sdk = meta.get('sdk')
    if sdk == 'manifest':
        args += ['--hl2sdk-root', str(deps), '--hl2sdk-manifest-path', str(sm / 'hl2sdk-manifests'), '--sdks=tf2']
    elif sdk == 'legacy':
        args += ['--hl2sdk-root', str(deps)]
        if project == 'Connect':
            args += ['--sdks=tf2']
    elif sdk == 'vscript':
        args += ['--sdk-root', str(deps), '--sdk=tf2']
    if meta.get('plugin'):
        args += ['--no-plugins']  # Same-version plugin is built once in the plugin matrix.
    if meta.get('auto_version'):
        args += ['--enable-auto-versioning']
    output.mkdir(parents=True, exist_ok=True)
    subprocess.run(args, cwd=output, check=True)
    subprocess.run(['ambuild'], cwd=output, check=True)
    return package_path(project, output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('version', 'build', 'verify'))
    parser.add_argument('project', choices=PROJECTS)
    parser.add_argument('--deps', type=Path, default=ROOT / 'deps')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--arch', choices=('x86', 'x86_64'))
    parser.add_argument('--platform', choices=('windows', 'linux'))
    args = parser.parse_args()
    if args.command == 'version':
        print(version(args.project))
        return
    if not args.arch:
        parser.error('--arch is required for build and verify')
    output = (args.output or ROOT / args.project / 'build').resolve()
    if args.command == 'build':
        build(args.project, output, args.deps.resolve(), args.arch)
    else:
        if not args.platform:
            parser.error('--platform is required for verify')
        verify(args.project, package_path(args.project, output), args.arch, args.platform)


if __name__ == '__main__':
    main()
