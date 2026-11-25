# SM-Extensions

Vendored SourceMod extensions for game-server maintenance. Each top-level project directory contains a snapshot of its upstream source, not a Git submodule. Upstream build files, notices, and license declarations are preserved. This initial import uses the current upstream default branches; the versions observed on an existing server are listed separately where they differ.

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

This is a source import only. No extension has been built, modernized, or installed by this import. Consult each project's upstream build instructions for its SDK requirements.

## Licensing

Each project remains under its upstream licensing terms, including any bundled third-party code. See the project's license files and source headers. Copies of the GPL-3.0 and LGPL-2.1 license texts are supplied under [LICENSES](LICENSES) for projects that declare those licenses in their source but do not ship a standalone copy. No new repository-wide license overrides the upstream terms.
