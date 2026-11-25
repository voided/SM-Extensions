#!/usr/bin/env python3
"""Build the pinned upstream static GNU libmicrohttpd library for Webcon."""
import argparse
import hashlib
import os
import shutil
import subprocess
import urllib.request
from pathlib import Path

VERSION = '1.0.10'
SHA256 = '04bfe8ef75db7d629a33de767599765cecadc56274a39822d5d081030d577685'
URL = f'https://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-{VERSION}.tar.gz'


def build(root, arch, platform):
    root.mkdir(parents=True, exist_ok=True)
    archive = root / f'libmicrohttpd-{VERSION}.tar.gz'
    if not archive.exists():
        urllib.request.urlretrieve(URL, archive)
    if hashlib.sha256(archive.read_bytes()).hexdigest() != SHA256:
        raise ValueError('libmicrohttpd archive checksum mismatch')
    source = root / f'libmicrohttpd-{VERSION}'
    if not source.exists():
        shutil.unpack_archive(str(archive), str(root))
    prefix = root / arch
    if platform == 'linux':
        work = root / f'build-{arch}'
        work.mkdir(exist_ok=True)
        bits = '32' if arch == 'x86' else '64'
        host = 'i686-linux-gnu' if arch == 'x86' else 'x86_64-linux-gnu'
        env = dict(os.environ, CC=f'{os.environ.get("CC", "clang")} -m{bits}', CFLAGS='-O2 -fPIC')
        configure = [str(source / 'configure'), f'--host={host}', f'--prefix={prefix}',
                     '--disable-shared', '--enable-static', '--with-pic', '--disable-https',
                     '--disable-curl', '--disable-doc', '--disable-examples']
        if arch == 'x86':
            # Debian 11's 32-bit glibc does not support 64-bit time_t.
            configure.append('--disable-year2038')
        subprocess.run(configure, cwd=work, env=env, check=True)
        subprocess.run(['make', f'-j{min(os.cpu_count() or 2, 8)}'], cwd=work, env=env, check=True)
        subprocess.run(['make', 'install'], cwd=work, env=env, check=True)
        library = prefix / 'lib/libmicrohttpd.a'
    else:
        # Use the upstream Visual Studio static-library project, with the
        # installed runner toolset rather than an old VS-specific version.
        solution = source / 'w32/VS-Any-Version/libmicrohttpd.sln'
        platform_name = 'Win32' if arch == 'x86' else 'x64'
        (prefix / 'lib').mkdir(parents=True, exist_ok=True)
        subprocess.run(['msbuild', str(solution), '/t:libmicrohttpd', '/m',
                        '/p:Configuration=Release-static', f'/p:Platform={platform_name}',
                        f'/p:OutDir={prefix / "lib"}{os.sep}'], check=True)
        (prefix / 'include').mkdir(exist_ok=True)
        shutil.copy2(source / 'src/include/microhttpd.h', prefix / 'include')
        library = prefix / 'lib/libmicrohttpd.lib'
    if not library.is_file() or not (prefix / 'include/microhttpd.h').is_file():
        raise FileNotFoundError(f'Incomplete libmicrohttpd installation: {prefix}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--arch', choices=('x86', 'x86_64'), required=True)
    parser.add_argument('--platform', choices=('linux', 'windows'), required=True)
    args = parser.parse_args()
    build(args.root.resolve(), args.arch, args.platform)
