# CStudioHdr::GetSharedPoseParameter Fix

Original SourceMod extension by Benoist3012. The compatibility port uses AMBuild 2.2 and the shared SafetyHook submodule, with current TF2 SDK types instead of the old duplicated studio header and virtual model layout. The hook guards invalid sequence indices and otherwise calls the original game routine, thereby retaining the current game behavior for invalid groups and local pose indices.

Supports native builds for x86 and x64 on Linux and Windows, with signatures checked against local TF2 dedicated-server binaries. CI builds both SourceMod 1.12 and 1.13.
