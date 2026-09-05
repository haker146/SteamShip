// LumaCore — Steam client hook layer for SteamShip.
// Copyright (c) 2026 haker146 (https://github.com/haker146).
// Distributed under the GNU General Public License v3 or later.
// See <https://www.gnu.org/licenses/> for the full license text.

#ifndef ORCHESTRATOR_H
#define ORCHESTRATOR_H

#include "core/entry.h"

namespace SteamUI {
    void CoreHook();
    void CoreUnhook();
}

namespace LumaCore {
    void Attach();
    void Detach();
}


#endif // ORCHESTRATOR_H
