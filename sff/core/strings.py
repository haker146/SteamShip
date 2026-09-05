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


import base64 as _b64

VERSION = "1.0.0"
# NOTE: Public key shared by oureveryday (https://github.com/SteamAutoCracks/Steam-auto-crack/issues/33)
_swak = b"MUREMDQ1MEE5OUY1NzM2OTNDRDAzMUVCQjE2MDkwN0Q="
STEAM_WEB_API_KEY = _b64.b64decode(_swak).decode()
GITHUB_USERNAME = "haker146"
REPO_NAME = "SteamShip"
# Update check source: https://github.com/haker146/SteamShip/releases/
GITHUB_UPDATE_USERNAME = "haker146"
REPO_UPDATE_NAME = "SteamShip"
RELEASE_PAGE_URL = "https://github.com/haker146/SteamShip/releases/"
WINDOWS_RELEASE_PREFIX = "0_windows_x86-64"
LINUX_RELEASE_PREFIX = "1_linux_x86-64"
