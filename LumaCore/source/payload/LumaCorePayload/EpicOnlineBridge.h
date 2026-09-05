// LumaCorePayload — injected into game processes for EOS bridge.
// Copyright (c) 2026 haker146 (https://github.com/haker146).
// Distributed under the GNU General Public License v3 or later.
// See <https://www.gnu.org/licenses/> for the full license text.

#pragma once

#include <windows.h>

namespace EosBridge {
    void InstallOn(HMODULE eosModule);
}
