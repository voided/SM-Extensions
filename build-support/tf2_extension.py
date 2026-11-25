"""AMBuild 2.2 support for simple, legacy TF2 extensions."""
import os
from pathlib import Path
from safetyhook import build_safetyhook


def configure(builder, name, sources, files, *, detours=False, safetyhook=False, config_dir='.'):
    root = Path(builder.sourcePath)
    sm = Path(builder.options.sm_path).resolve()
    mms = Path(builder.options.mms_path).resolve()
    sdk_root = Path(builder.options.hl2sdk_root).resolve()
    targets = [builder.DetectCxx(target_arch=arch) for arch in builder.options.targets.split(',')]
    helpers = builder.Eval(str(sm / 'hl2sdk-manifests/SdkHelpers.ambuild'), {'Project': 'sm-extension'})
    helpers.find_sdk_path = lambda sdk: str(sdk_root / ('hl2sdk-' + sdk))
    helpers.findSdks(builder, targets, ['tf2'])
    sdk = helpers.sdks['tf2']

    for cxx in targets:
        if cxx.like('gcc'):
            cxx.defines += ['HAVE_STDINT_H']
            cxx.cflags += ['-pipe', '-fno-strict-aliasing', '-fvisibility=hidden']
            cxx.cxxflags += ['-std=c++17', '-fvisibility-inlines-hidden']
            cxx.linkflags += ['-static-libgcc', '-static-libstdc++']
            if builder.options.debug:
                cxx.cflags += ['-g']
            if builder.options.opt:
                cxx.cflags += ['-O3']
        elif cxx.like('msvc'):
            cxx.defines += ['_CRT_SECURE_NO_WARNINGS', '_CRT_NONSTDC_NO_WARNINGS', '_ITERATOR_DEBUG_LEVEL=0']
            cxx.cflags += ['/W3', '/MTd' if builder.options.debug else '/MT']
            if builder.options.debug:
                cxx.cflags += ['/Zi']
                cxx.linkflags += ['/DEBUG']
            cxx.cxxflags += ['/EHsc', '/std:c++17']
            if builder.options.opt:
                cxx.cflags += ['/Ox']
        cxx.defines += ['DEBUG', '_DEBUG'] if builder.options.debug else ['NDEBUG']

    safetyhook_tasks = []
    if detours or safetyhook:
        builder.AddConfigureFile(str(root.parent / 'build-support/safetyhook.py'))
        safetyhook_include, safetyhook_tasks = build_safetyhook(builder, targets)

    project = builder.LibraryProject(name)
    project.sources += [str(root / s) for s in sources]
    project.sources += [str(sm / 'public/smsdk_ext.cpp')]
    if detours:
        project.sources += [str(sm / 'public/CDetour/detours.cpp')]
    for cxx in targets:
        binary = project.Configure(cxx, name + '.ext.' + sdk['extension'], cxx.target.arch)
        compiler = binary.compiler
        compiler.defines += ['SOURCEMOD_BUILD']
        compiler.defines += ['SE_{}={}'.format(manifest['define'], manifest['code']) for manifest in helpers.sdk_manifests]
        helpers.configureCxx(builder, binary, sdk)
        compiler.cxxincludes += [str(p) for p in (
            root, root / config_dir, sm / 'public', sm / 'public/extensions',
            sm / 'public/amtl', sm / 'public/amtl/amtl', sm / 'sourcepawn/include',
            mms / 'core', mms / 'core/sourcehook',
        )]
        if detours or safetyhook:
            compiler.cxxincludes += [safetyhook_include]
            compiler.linkflags += [next(task.binary for task in safetyhook_tasks if task.target.arch == cxx.target.arch)]
    binaries = builder.Add(project)

    builder.SetBuildFolder('package')
    for folder, paths in files.items():
        output = builder.AddFolder(os.path.join('addons/sourcemod', folder))
        for path in paths:
            builder.AddCopy(str(root / path), output)
    for binary in binaries:
        folder = 'addons/sourcemod/extensions'
        if binary.target.arch == 'x86_64':
            folder += '/x64'
        builder.AddCopy(binary.binary, builder.AddFolder(folder))
