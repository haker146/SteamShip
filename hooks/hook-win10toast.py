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

# PyInstaller hook for win10toast
# This ensures win10toast data files are properly included

from PyInstaller.utils.hooks import collect_data_files, copy_metadata

# Collect all data files from win10toast package
datas = collect_data_files('win10toast')

# Copy metadata to help pkg_resources find the package
datas += copy_metadata('win10toast')

# pkg_resources.py2_warn removed: module does not exist in newer setuptools (avoids "hidden import not found" warning)
hiddenimports = []
