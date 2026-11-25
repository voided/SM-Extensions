# SM-Extensions

Vendored SourceMod extensions for game-server maintenance. Each top-level project directory contains a snapshot of its upstream source, not a Git submodule. Upstream notices and license declarations are preserved; build definitions may be updated independently to support current SourceMod versions. This initial import uses the current upstream default branches; the versions observed on an existing server are listed separately where they differ.

## Upstream inventory

| Project / directory | Upstream | Imported revision | Imported version / notes |
| --- | --- | --- | --- |
| [Accelerator](Accelerator) | [asherkin/accelerator](https://github.com/asherkin/accelerator) | `a4dbe6f97580f856ed7a2f8aace4da735ae6b9dd` | 2.6.0 |
| [Connect](Connect) | [asherkin/connect](https://github.com/asherkin/connect) | `3fe8d3ae8b09c72c49622e188915ab7a64f76426` | 1.4.0 |
| [ConsoleCleaner](ConsoleCleaner) | [accelerator74/Cleaner](https://github.com/accelerator74/Cleaner) | `a4a80f08dbc60c01cbee028ba0c9c6412a4f5cd7` | 1.5.0; successor to [Equinox Console Cleaner](https://forums.alliedmods.net/showthread.php?t=195008). The reported 1.4.0 corresponds to upstream commit `d1809a7`. |
| [LoadSoundScript](LoadSoundScript) | [haxtonsale/LoadSoundScript](https://github.com/haxtonsale/LoadSoundScript) | `c71f4a448668308521fcc138b6ef58e2ac03caa9` | 1.1.0 |
| [PoseParameterFix](PoseParameterFix) | [Kenzzer/JetPack_Fix](https://github.com/Kenzzer/JetPack_Fix) / [release thread](https://forums.alliedmods.net/showthread.php?t=309821) | `72005c81167a3d486c844b774b2eead5cbd0a5d2` | CStudioHdr::GetSharedPoseParameter Fix 0.1; upstream precompiled .so and .dll omitted. |
| [SMJansson](SMJansson) | [davenonymous/SMJansson](https://github.com/davenonymous/SMJansson) | `49886bbc0f8520b4c335a12e974c1aa044aa5b8f` | 2.15.1/1 |
| [Socket](Socket) | [nefarius/sm-ext-socket](https://github.com/nefarius/sm-ext-socket) | `ed6bf7a12bd3f801610592301e12062b367fa27b` | 3.0.2; [community Linux build notes](https://github.com/valedar/VT5514/blob/main/compile_socket.md) (not applied). |
| [SourceScramble](SourceScramble) | [nosoop/SMExt-SourceScramble](https://github.com/nosoop/SMExt-SourceScramble) | `eb31a8911f3634020f74e53d5ed6b1d8706bf2af` | 0.8.2 |
| [TFEconDynamic](TFEconDynamic) | [nosoop/SMExt-TFEconDynamic](https://github.com/nosoop/SMExt-TFEconDynamic) | `3542b83c584d9b663a946c59bf9b5c606d4a4946` | 0.1.0 |
| [TFMaxSpeedDetour](TFMaxSpeedDetour) | [nosoop/SMExt-TFMaxSpeedDetour](https://github.com/nosoop/SMExt-TFMaxSpeedDetour) | `6a4ad392a587a1f1f0290dbbd612559248414226` | TF2 CalculateMaxSpeed Detour 1.0.4 |
| [TFMaxVoiceSpeakDelayUnlimiter](TFMaxVoiceSpeakDelayUnlimiter) | [sigsegv-mvm/TFMaxVoiceSpeakDelayUnlimiter](https://github.com/sigsegv-mvm/TFMaxVoiceSpeakDelayUnlimiter) | `68bf79d3aac8ff47b5aabdb89668cc9fd86ebae7` | 20171110-1 |
| [VScript](VScript) | [Mikusch/vscript-ext](https://github.com/Mikusch/vscript-ext) | `10bcc565f5906a12a54ec1a77422b22559d9642f` | 1.3.0; reported version 1.1.0 is [tagged upstream](https://github.com/Mikusch/vscript-ext/tree/1.1.0). |
| [Webcon-Conplex](Webcon-Conplex) | [asherkin/webcon](https://github.com/asherkin/webcon) | `6a8ba6b51ec199e861d7420afe2309e157a2bd81` | Webcon and Conplex share build scripts and are preserved together. |

### Still to identify

- `teamnumproxy` (Manual Build), description: Provides safe proxying of CTFPlayer::m_iTeamNum. No verified public source repository found; no replacement implementation imported.

## Dependencies and build status

Accelerator and VScript have upstream-pinned third-party Git submodules, retained as dependencies at their original paths. Initialize them with `git submodule update --init --recursive` after cloning. The extensions themselves are ordinary tracked source directories.

### GitHub Actions

Each enabled extension has its own [workflow](.github/workflows), path filters, manual dispatch, and release. The workflows share the same AMBuild **2.2** build and release jobs, modeled on SM-TF2Items and CollisionHook.

The native matrix is SourceMod **1.12** (`1.12-dev`) and **1.13** (`master`), Windows and Linux, and x86 and x86_64 where the extension has matching gamedata. Engine-specific extensions are built against the TF2 SDK; generic extensions build without an engine SDK. Metamod:Source uses `1.12-dev` where required. Linux uses the AlliedModders Debian 11 / Clang 22 build container, and Windows uses MSVC. SourceScramble and TFEconDynamic also compile their bundled SourcePawn plugins once per matching SourceMod version and include them in the native packages.

| Extension | Workflow | Linux | Windows |
| --- | --- | --- | --- |
| Accelerator | [accelerator.yml](.github/workflows/accelerator.yml) | x86, x64 | x86, x64 |
| Connect | [connect.yml](.github/workflows/connect.yml) | x86, x64 | x86, x64 |
| ConsoleCleaner | [console-cleaner.yml](.github/workflows/console-cleaner.yml) | x86, x64 | x86, x64 |
| LoadSoundScript | [load-soundscript.yml](.github/workflows/load-soundscript.yml) | x86, x64 | x86, x64 |
| SMJansson | [smjansson.yml](.github/workflows/smjansson.yml) | x86, x64 | x86, x64 |
| SourceScramble | [source-scramble.yml](.github/workflows/source-scramble.yml) | x86, x64 | x86, x64 |
| TFEconDynamic | [tf-econ-dynamic.yml](.github/workflows/tf-econ-dynamic.yml) | x86, x64 | x86, x64 |
| TFMaxSpeedDetour | [tf-max-speed-detour.yml](.github/workflows/tf-max-speed-detour.yml) | x86 | x86 |
| TFMaxVoiceSpeakDelayUnlimiter | [tf-max-voice-speak-delay-unlimiter.yml](.github/workflows/tf-max-voice-speak-delay-unlimiter.yml) | x86, x64 | x86, x64 |
| VScript | [vscript.yml](.github/workflows/vscript.yml) | x86, x64 | x86, x64 |

Builds upload an installable `addons/` tree for each matrix entry. On `main` pushes and manual runs of `main`, once every build in the extension's matrix succeeds, the workflow merges the supported architecture trees and publishes four archives (Linux tar.gz and Windows zip for each SourceMod version). Tags are namespaced as `<Extension>-v<upstream-version>.<repository-revision-count>` so independent extensions do not collide; e.g. `SMJansson-v2.15.1-1.2`. Branch and pull-request builds do not publish releases.

To build an enabled extension locally, install AMBuild 2.2 or newer and the appropriate native toolchain, then prepare a dependency directory with the same checkout names as used by CI (`sourcemod`, `metamod-source` if required, and `hl2sdk-tf2` for engine-dependent projects). For example:

```sh
python -m pip install git+https://github.com/alliedmodders/ambuild.git
python .github/scripts/build_extension.py build TFMaxSpeedDetour --deps /path/to/deps --arch x86
python .github/scripts/build_extension.py verify TFMaxSpeedDetour --arch x86 --platform linux
```

For projects with bundled SourcePawn plugins, invoke the matching SourcePawn compiler and copy the `.smx` into the package's `addons/sourcemod/plugins` directory, as the CI plugin job does.

### Deferred CI

| Extension | Reason |
| --- | --- |
| PoseParameterFix | Legacy AMBuild scripts and a locally bundled CDetour/assembly implementation from before the current SourceMod SafetyHook API; needs a proper compatibility port and current gamedata/layout review. |
| Socket | Hard-coded 32-bit Makefile and old MSVC project, bundled legacy SourceMod SDK shim and Boost.Asio/Boost.Thread dependency; needs a modern AMBuild 2.2 and dependency port for both platforms. |
| Webcon and Conplex | Shared legacy build requiring older SourceMod header paths and detour APIs, a bundled historical libmicrohttpd and platform networking code; needs a coordinated modernization before independent releases. |

The build matrix validates compilation and package layout, not game-server behavior. TFMaxSpeedDetour compiles for x64, but its upstream gamedata only supplies x86 signature keys; x64 is intentionally excluded from CI until the gamedata is updated. Other gamedata and ABI compatibility still require runtime validation before deployment.

## Licensing

Each project remains under its upstream licensing terms, including any bundled third-party code. See the project's license files and source headers. Copies of the GPL-3.0 and LGPL-2.1 license texts are supplied under [LICENSES](LICENSES) for projects that declare those licenses in their source but do not ship a standalone copy. No new repository-wide license overrides the upstream terms.
