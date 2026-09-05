// LumaCore - Steam client hook layer for SteamShip.
// Copyright (c) 2026 haker146 (https://github.com/haker146).
// Distributed under the GNU General Public License v3 or later.
// See <https://www.gnu.org/licenses/> for the full license text.

#include "hooks/client/PacketRouter.h"
#include "hooks/client/NetPacket.h"

namespace PacketRouter {
    void Install() {
        NetPacket::Install();
    }

    void Uninstall() {
        NetPacket::Uninstall();
    }
}
