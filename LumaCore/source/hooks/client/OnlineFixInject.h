// LumaCore - Steam client hook layer for SteamShip.
// Copyright (c) 2026 haker146 (https://github.com/haker146).
// Distributed under the GNU General Public License v3 or later.
// See <https://www.gnu.org/licenses/> for the full license text.

#pragma once

#include "core/entry.h"

#include <cstdint>
#include <string>

namespace OnlineFixInject {
    void Install();
    void Uninstall();

    void QueueInjection(const char* exePath, AppId_t realAppId);
    void RecordNoEos(uint32_t pid, const std::string& imageName, AppId_t realAppId);
    bool TryFallbackInject(uint32_t pid, const std::string& imageName, AppId_t realAppId);
}
