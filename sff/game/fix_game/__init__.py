# SteamShip - Steam game setup and manifest tool (SFF)
# Copyright (c) 2026 haker146 (https://github.com/haker146)
#
# This file is part of SteamShip.
#
# SteamShip is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SteamShip is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SteamShip.  If not, see <https://www.gnu.org/licenses/>.

"""
Fix Game pipeline — makes downloaded games playable.

Orchestrates: DRM detection → Goldberg update → config generation →
SteamStub unpacking → Goldberg application → Launch.bat generation.
"""

from sff.game.fix_game.service import FixGameService
from sff.game.fix_game.cache import FixGameCache
from sff.game.fix_game.goldberg_updater import GoldbergUpdater
from sff.game.fix_game.config_generator import GoldbergConfigGenerator
from sff.game.fix_game.steamstub_unpacker import SteamStubUnpacker
from sff.game.fix_game.goldberg_applier import GoldbergApplier

__all__ = [
    "FixGameService",
    "FixGameCache",
    "GoldbergUpdater",
    "GoldbergConfigGenerator",
    "SteamStubUnpacker",
    "GoldbergApplier",
]
