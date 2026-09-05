// LumaCore - Steam client hook layer for SteamShip.
// Copyright (c) 2026 haker146 (https://github.com/haker146).
// Distributed under the GNU General Public License v3 or later.
// See <https://www.gnu.org/licenses/> for the full license text.

#pragma once

#include "Steam/Types.h"

#include <optional>

namespace AsyncTicketMap {
    void Remember(SteamAPICall_t call, AppId_t appId);
    std::optional<AppId_t> Claim(SteamAPICall_t call);
    void Forget(SteamAPICall_t call);
    void Reset();
}
