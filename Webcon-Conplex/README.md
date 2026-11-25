# Webcon and Conplex

Two separate SourceMod extensions with separate packages and releases. Conplex multiplexes the game's existing TCP console listener; Webcon depends on Conplex and exposes the original HTTP plugin API. The modernized build uses AMBuild 2.2 with the selected SM 1.12 or 1.13 SDK. Conplex uses the shared SafetyHook submodule directly and refuses to load if a required gamedata signature is missing, rather than hooking unrelated sockets or bypassing the engine's failed-auth handling. It compiles with AlliedModders' TF2 HL2SDK and its SDK manifests for the target architecture, using the SDK's `CUtlVector`, `CUtlMemory`, and `netadr_t` types and tier1 implementation instead of the old bundled headers. Webcon has no HL2SDK dependency.

## Supported targets

TF2 on Linux x86 and x86_64. Windows build configuration is retained, but Windows CI/release support is deferred pending validation of the current Conplex gamedata and socket ABI. The extension does not implement HTTPS; the plain HTTP functionality is unchanged in that respect.

## libmicrohttpd dependency

Webcon statically links the official [GNU libmicrohttpd 1.0.10 source release](https://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-1.0.10.tar.gz), pinned by SHA-256 in `.github/scripts/build_microhttpd.py`. Its outdated embedded copy has been removed. CI builds the library for the same architecture as the extension and disables TLS, documentation, examples and curl-based tests. On Windows the dependency helper uses the upstream Visual Studio static-library project. The dependency is LGPL-2.1-or-later; the corresponding source release is available at the link above, and the license is available in the repository's `LICENSES` directory.

For local Linux builds from the repository root, prepare the SourceMod checkout as `deps/sourcemod` and AlliedModders' TF2 HL2SDK as `deps/hl2sdk-tf2`, then build the dependency using:

```sh
python .github/scripts/build_microhttpd.py --root deps/microhttpd --arch x86_64 --platform linux
python .github/scripts/build_extension.py build Conplex --arch x86_64
python .github/scripts/build_extension.py build Webcon --arch x86_64
```

Each component's package contains its own native extension and SourcePawn include files. Install Conplex before Webcon. No sample web administration plugins are auto-installed.
