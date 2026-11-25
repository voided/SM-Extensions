"""AMBuild 2.2 support for simple, legacy TF2 extensions."""
import os
import shutil
from pathlib import Path
from types import SimpleNamespace


def configure(builder, name, sources, files, *, detours=False, config_dir='.'):
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
    if detours:
        # Use the matching SourceMod SDK's CDetour implementation and dependencies.
        # Build in an isolated copy, as the upstream SafetyHook AMBuilder is relative to its source directory.
        safetyhook = root / 'safetyhook'
        shutil.copytree(sm / 'public/safetyhook', safetyhook, dirs_exist_ok=True)
        shim = SimpleNamespace(all_targets=targets, libsafetyhook=[])
        builder.Build('safetyhook/AMBuilder', {'SafetyHook': shim})
        safetyhook_tasks = shim.libsafetyhook

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
        if detours:
            compiler.cxxincludes += [str(root / 'safetyhook/include')]
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
