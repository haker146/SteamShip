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
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def _atomic_write(target: Path, payload: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(target)


def block_updates(steam_path: Path) -> None:
    target = steam_path / "steam.cfg"
    _atomic_write(target, "BootStrapperInhibitAll=Enable\n")


def unblock_updates(steam_path: Path) -> None:
    target = steam_path / "steam.cfg"
    _atomic_write(target, "BootStrapperInhibitAll=False\n")
