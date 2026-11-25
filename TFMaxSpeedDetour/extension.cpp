/**
 * vim: set ts=4 :
 * =============================================================================
 * TF2 Calculate Max Speed Detour Extension
 * Copyright (C) 2018 nosoop.  All rights reserved.
 * =============================================================================
 *
 * This program is free software; you can redistribute it and/or modify it under
 * the terms of the GNU General Public License, version 3.0, as published by the
 * Free Software Foundation.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License along with
 * this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * As a special exception, AlliedModders LLC gives you permission to link the
 * code of this program (as well as its derivative works) to "Half-Life 2," the
 * "Source Engine," the "SourcePawn JIT," and any Game MODs that run on software
 * by the Valve Corporation.  You must obey the GNU General Public License in
 * all respects for all other code used.  Additionally, AlliedModders LLC grants
 * this exception to all derivative works.  AlliedModders LLC defines further
 * exceptions, found in LICENSE.txt (as of this writing, version JULY-31-2007),
 * or <http://www.sourcemod.net/license.php>.
 *
 * Version: $Id$
 */

#include "extension.h"
#include <cstdio>

/**
 * @file extension.cpp
 * @brief Implement extension code here.
 */

TF2MaxSpeedDetour g_TF2MaxSpeedDetour;		/**< Global singleton for extension's main interface */

SMEXT_LINK(&g_TF2MaxSpeedDetour);

CDetour *detour_CTFPlayer_CalculateMaxSpeed = nullptr;

IForward *g_calculateMaxSpeedForward = NULL;

DETOUR_DECL_MEMBER1(CTFPlayer_CalculateMaxSpeed, float, bool, reentrant) {
	float flOrigResult = DETOUR_MEMBER_CALL(CTFPlayer_CalculateMaxSpeed)(reentrant);
	
	// inner call
	if (reentrant) {
		return flOrigResult;
	}
	
	// prevent calling forward when the server is shutting down
	if (!g_pSM->IsMapRunning()) {
		return flOrigResult;
	}
	
	float flResult = flOrigResult;
	
	cell_t playerCell = gamehelpers->EntityToBCompatRef((CBaseEntity *)this);
	
	// prevent calling on invalid player (????)
	IGamePlayer *player = playerhelpers->GetGamePlayer(playerCell);
	if (!player || !player->IsInGame()) {
		return flOrigResult;
	}
	
	g_calculateMaxSpeedForward->PushCell(playerCell);
	g_calculateMaxSpeedForward->PushFloatByRef(&flResult);
	
	cell_t result = 0;
	g_calculateMaxSpeedForward->Execute(&result);
	
	if (result == Pl_Continue) {
		flResult = flOrigResult;
	}
	
	// TODO post forward?
	
	return flResult;
}

bool TF2MaxSpeedDetour::SDK_OnLoad(char *error, size_t maxlength, bool late) {
	IGameConfig *pGameConf = NULL;
	
	if (!gameconfs->LoadGameConfigFile("tf2.calcmaxspeed", &pGameConf, error, maxlength)) {
		return false;
	}
	
	CDetourManager::Init(g_pSM->GetScriptingEngine(), pGameConf);
	
	detour_CTFPlayer_CalculateMaxSpeed =
			DETOUR_CREATE_MEMBER(CTFPlayer_CalculateMaxSpeed,
			"CTFPlayer::TeamFortress_CalculateMaxSpeed()");
	
	gameconfs->CloseGameConfigFile(pGameConf);
	if (!detour_CTFPlayer_CalculateMaxSpeed) {
		std::snprintf(error, maxlength, "Could not create TeamFortress_CalculateMaxSpeed detour");
		return false;
	}
	
	// Action TF2_OnCalculateMaxSpeed(int client, float &flMaxSpeed);
	g_calculateMaxSpeedForward = forwards->CreateForward("TF2_OnCalculateMaxSpeed",
			ET_Hook, 2, NULL, Param_Cell, Param_FloatByRef);
	if (!g_calculateMaxSpeedForward) {
		detour_CTFPlayer_CalculateMaxSpeed->Destroy();
		detour_CTFPlayer_CalculateMaxSpeed = nullptr;
		std::snprintf(error, maxlength, "Could not create TF2_OnCalculateMaxSpeed forward");
		return false;
	}
	
	detour_CTFPlayer_CalculateMaxSpeed->EnableDetour();
	if (!detour_CTFPlayer_CalculateMaxSpeed->IsEnabled()) {
		SDK_OnUnload();
		std::snprintf(error, maxlength, "Could not enable TeamFortress_CalculateMaxSpeed detour");
		return false;
	}
	
	return true;
}

void TF2MaxSpeedDetour::SDK_OnUnload() {
	if (detour_CTFPlayer_CalculateMaxSpeed) {
		if (detour_CTFPlayer_CalculateMaxSpeed->IsEnabled()) {
			detour_CTFPlayer_CalculateMaxSpeed->DisableDetour();
		}
		detour_CTFPlayer_CalculateMaxSpeed->Destroy();
		detour_CTFPlayer_CalculateMaxSpeed = nullptr;
	}
	if (g_calculateMaxSpeedForward) {
		forwards->ReleaseForward(g_calculateMaxSpeedForward);
		g_calculateMaxSpeedForward = nullptr;
	}
}
