// LumaCore - Steam client hook layer for SteamShip.
// Copyright (c) 2026 haker146 (https://github.com/haker146).
// Distributed under the GNU General Public License v3 or later.
// See <https://www.gnu.org/licenses/> for the full license text.

#pragma once

#include "hooks/client/PipeWatch.h"

namespace AuthWindow {

    void Reset();
    void OnGamePipe(const PipeWatch::ProcessSnapshot& snapshot, CSteamPipeClient* pipe);
    bool IsSelectedPipe(const CSteamPipeClient* pipe);

}
