# SteamShip - Steam game setup and manifest tool (SFF)
# Copyright (c) 2026 haker146 (https://github.com/haker146)
# SteamShip fork — additional changes Copyright (c) 2026 haker146
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

"""SteamID-keyed cloud/local save prefixes with SteamShip fallback reads."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

from sff.brand import (
    CLOUD_FOLDER,
    CLOUD_FOLDER_FORK,
    CLOUD_FOLDER_LEGACY,
    UNLINKED_BUCKET,
    legacy_appdata_dir,
    save_account_id,
)
from sff.core.utils import sff_data_dir

logger = logging.getLogger(__name__)

_MIGRATED_MARKER = ".steamship_save_migrated"


def account_bucket() -> str:
    return save_account_id() or UNLINKED_BUCKET


def cloud_relative_root() -> str:
    """SteamShip/<steamid64-or-unlinked>"""
    return f"{CLOUD_FOLDER}/{account_bucket()}"


def rclone_game_path(remote_dest: str, label: str) -> str:
    base = (remote_dest or "").rstrip("/")
    return f"{base}/{cloud_relative_root()}/{label}"


def rclone_legacy_roots(remote_dest: str) -> list[str]:
    base = (remote_dest or "").rstrip("/")
    return [
        f"{base}/{CLOUD_FOLDER_LEGACY}",
        f"{base}/{CLOUD_FOLDER_LEGACY}/Games",
        f"{base}/SteaMidra/Saves",
        f"{base}/{CLOUD_FOLDER_FORK}",
    ]


def local_account_backup_dir(root: Path) -> Path:
    """<root>/<steamid>/ with one-time copy from the old flat tree."""
    bucket = account_bucket()
    keyed = root / bucket
    keyed.mkdir(parents=True, exist_ok=True)
    _migrate_flat_backups(root, keyed)
    _maybe_copy_legacy_appdata(keyed)
    return keyed


def _migrate_flat_backups(root: Path, keyed: Path) -> None:
    marker = keyed / _MIGRATED_MARKER
    if marker.exists():
        return
    try:
        if not root.is_dir():
            marker.write_text("ok", encoding="utf-8")
            return
        for child in root.iterdir():
            if not child.is_dir():
                continue
            if child.name in {UNLINKED_BUCKET, keyed.name} or child.name.startswith("."):
                continue
            if child.name == CLOUD_FOLDER_LEGACY:
                continue
            dest = keyed / child.name
            if dest.exists():
                continue
            shutil.copytree(child, dest, dirs_exist_ok=True)
        marker.write_text("ok", encoding="utf-8")
    except Exception as exc:
        logger.debug("save backup migration skipped: %s", exc)


def _maybe_copy_legacy_appdata(keyed: Path) -> None:
    legacy = legacy_appdata_dir() / "save_backups"
    if not legacy.is_dir():
        return
    try:
        for child in legacy.iterdir():
            if not child.is_dir():
                continue
            dest = keyed / child.name
            if dest.exists():
                continue
            shutil.copytree(child, dest, dirs_exist_ok=True)
    except Exception as exc:
        logger.debug("legacy APPDATA save read skipped: %s", exc)


def extra_local_scan_roots(primary: Path) -> list[Path]:
    roots = [primary]
    install_flat = sff_data_dir() / "save_backups"
    if install_flat not in roots:
        roots.append(install_flat)
    legacy = legacy_appdata_dir() / "save_backups"
    if legacy not in roots:
        roots.append(legacy)
    return roots
