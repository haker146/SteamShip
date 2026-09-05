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

"""Public SteamShip identity. Internal packages stay `sff` / LumaCore."""

from __future__ import annotations

import os
import re
from pathlib import Path

APP_NAME = "SteamShip"
APP_NAME_LEGACY = "SteaMidra"
RUNTIME_DISPLAY = "SteamShip runtime"
UNLINKED_BUCKET = "unlinked"

DRIVE_ROOT_NAME = "SteamShip"
DRIVE_ROOT_LEGACY = "SteaMidra Backups"
CLOUD_FOLDER = "SteamShip"
CLOUD_FOLDER_LEGACY = "SteaMidraAllSaves"
CLOUD_FOLDER_FORK = "Steamship"  # pre-1.0 fork folder name

# First hop for LumaCore pattern TOMLs (branch `pattern`, same layout as Steam-Auto-PT).
# DLL releases stay on KoriaPolis/LumaCore.
PATTERN_MIRROR_REPO_DEFAULT = os.environ.get("STEAMSHIP_PT_REPO", "haker146/SteamShip").strip()
PATTERN_MIRROR_BRANCH = os.environ.get("STEAMSHIP_PT_BRANCH", "pattern").strip() or "pattern"

_STEAMID64_RE = re.compile(r"^7656119\d{10}$")


def is_steamid64(value: str | None) -> bool:
    return bool(value and _STEAMID64_RE.match(str(value).strip()))


def save_account_id() -> str:
    """SteamID64 when logged in via OpenID, otherwise the unlinked bucket."""
    try:
        from sff.core.storage.settings import get_setting
        from sff.core.structs import Settings

        sid = str(get_setting(Settings.STEAM_OPENID_ID) or "").strip()
        if is_steamid64(sid):
            return sid
    except Exception:
        pass
    return UNLINKED_BUCKET


def pattern_mirror_repo() -> str:
    try:
        from sff.core.storage.settings import get_setting
        from sff.core.structs import Settings

        configured = str(get_setting(Settings.STEAMSHIP_PT_REPO) or "").strip()
        if configured and "/" in configured:
            return configured
    except Exception:
        pass
    return PATTERN_MIRROR_REPO_DEFAULT


def pattern_mirror_template() -> str:
    repo = pattern_mirror_repo()
    if not repo or "/" not in repo:
        return ""
    branch = PATTERN_MIRROR_BRANCH
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{{subdir}}/{{sha}}.toml"


def bundled_pattern_dir() -> Path:
    from sff.core.utils import root_folder

    return root_folder() / "pattern"


def legacy_appdata_dir() -> Path:
    appdata = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
    return Path(appdata) / APP_NAME_LEGACY
