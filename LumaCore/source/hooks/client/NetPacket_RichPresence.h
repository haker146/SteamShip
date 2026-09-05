// LumaCore — Steam client hook layer for SteamShip.
// Copyright (c) 2026 haker146 (https://github.com/haker146).
// Distributed under the GNU General Public License v3 or later.
// See <https://www.gnu.org/licenses/> for the full license text.

#pragma once

#include "Steam/Types.h"

struct CNetPacket;

namespace RichPresence {
    bool HandleRecv(const uint8_t* pBody, uint32_t cbBody,
                    uint8_t* pOutBuf, uint32_t outBufSize, uint32_t* pOutSize);
    void TrackGamesPlayed(const uint8_t* pBody, uint32_t cbBody,
                          const uint8_t* pHdr, uint32_t cbHdr);
    void TrackUpload(const uint8_t* pBody, uint32_t cbBody);
    void DeliverPending(void* pThis, CNetPacket* pPacket,
                        bool (*callOriginal)(void*, CNetPacket*));
}
