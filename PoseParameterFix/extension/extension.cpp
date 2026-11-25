#include "extension.h"
#include <studio.h>
#include <safetyhook.hpp>
#include <cstdio>
#include <utility>

static safetyhook::InlineHook poseParameterHook;
SMExt g_Ext;
SMEXT_LINK(&g_Ext);

// Modern TF2 already validates the pose and group. Guard the sequence before
// calling the original implementation, retaining its return-value semantics.
#if defined(_WIN32) && defined(_M_IX86)
static int __fastcall GetSharedPoseParameter(const CStudioHdr *studio, void *, int sequence, int localPose)
#else
static int GetSharedPoseParameter(const CStudioHdr *studio, int sequence, int localPose)
#endif
{
    const virtualmodel_t *model = studio->GetVirtualModel();
    if (model && localPose != -1 && !model->m_seq.IsValidIndex(sequence))
        return -1;

#if defined(_WIN32) && defined(_M_IX86)
    return poseParameterHook.thiscall<int>(studio, sequence, localPose);
#else
    return poseParameterHook.call<int>(studio, sequence, localPose);
#endif
}

bool SMExt::SDK_OnLoad(char *error, size_t maxlength, bool late)
{
    IGameConfig *config = nullptr;
    if (!gameconfs->LoadGameConfigFile("poseparameter_fix", &config, error, maxlength))
        return false;

    void *address = nullptr;
    const bool found = config->GetMemSig("CStudioHdr::GetSharedPoseParameter", &address);
    gameconfs->CloseGameConfigFile(config);
    if (!found || !address) {
        std::snprintf(error, maxlength, "Could not resolve CStudioHdr::GetSharedPoseParameter");
        return false;
    }

    auto hook = safetyhook::InlineHook::create(address, GetSharedPoseParameter,
                                              safetyhook::InlineHook::Flags::StartDisabled);
    if (!hook) {
        std::snprintf(error, maxlength, "Could not create pose parameter hook");
        return false;
    }
    poseParameterHook = std::move(hook.value());
    if (!poseParameterHook.enable()) {
        poseParameterHook.reset();
        std::snprintf(error, maxlength, "Could not enable pose parameter hook");
        return false;
    }
    return true;
}

void SMExt::SDK_OnUnload()
{
    poseParameterHook.reset();
}
