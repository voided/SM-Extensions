"""Build the shared, pinned AlliedModders SafetyHook submodule with AMBuild."""
from pathlib import Path


def build_safetyhook(builder, targets):
    root = Path(builder.sourcePath).parent / 'third_party/safetyhook'
    if not (root / 'AMBuilder').is_file():
        raise FileNotFoundError('Initialize SafetyHook with: git submodule update --init -- third_party/safetyhook')
    builder.AddConfigureFile(str(root / 'AMBuilder'))

    # AMBuild maps child script paths to build folders, so use absolute source
    # paths instead of creating a child build outside the extension's source tree.
    # These sources and compiler flags follow the pinned upstream AMBuilder.
    project = builder.StaticLibraryProject('safetyhook')
    project.sources += [str(root / 'src' / name) for name in (
        'allocator.cpp', 'easy.cpp', 'inline_hook.cpp', 'mid_hook.cpp',
        'utility.cpp', 'vmt_hook.cpp',
    )]
    project.sources += [str(root / 'zydis/Zydis.c')]

    for target in targets:
        binary = project.Configure(target, project.name, target.target.arch)
        compiler = binary.compiler
        compiler.cxxflags = []
        compiler.cflags = []
        compiler.defines = []
        compiler.includes = []
        compiler.cxxincludes = []
        if compiler.target.platform == 'windows':
            compiler.cflags += ['/W4']
            compiler.cxxflags += ['/EHsc', '/permissive-', '/w14640', '/std:c++17']
            binary.sources += [str(root / 'src/os.windows.cpp')]
        elif compiler.target.platform == 'linux':
            compiler.cflags += ['-Werror', '-Wall', '-Wextra', '-pedantic', '-Wshadow',
                                '-Wno-unused-const-variable', '-Wno-unused-function', '-fPIC']
            compiler.cxxflags += ['-Wnon-virtual-dtor', '-Wno-format', '-std=c++17']
            binary.sources += [str(root / 'src/os.linux.cpp')]
        else:
            raise ValueError(f'Unsupported SafetyHook platform: {compiler.target.platform}')
        compiler.includes += [str(root / 'include'), str(root / 'zydis')]

    return str(root / 'include'), builder.Add(project)
