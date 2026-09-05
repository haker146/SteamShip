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

"""Steam OpenID 2.0 login. Stores SteamID64 + persona for Drive/rclone keys."""

from __future__ import annotations

import logging
import threading
import urllib.parse
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

import httpx

from sff.brand import APP_NAME, is_steamid64

logger = logging.getLogger(__name__)

_STEAM_OPENID = "https://steamcommunity.com/openid/login"
_CLAIMED_PREFIX = "https://steamcommunity.com/openid/id/"
_XML_NS = "{http://steamcommunity.com/public/xml/steam/}"


def steam_account_dict() -> dict:
    try:
        from sff.core.storage.settings import get_setting
        from sff.core.structs import Settings

        sid = str(get_setting(Settings.STEAM_OPENID_ID) or "").strip()
        if not is_steamid64(sid):
            return {"linked": False, "steamid64": "", "persona": "", "avatar": ""}
        return {
            "linked": True,
            "steamid64": sid,
            "persona": str(get_setting(Settings.STEAM_PERSONA) or "").strip(),
            "avatar": str(get_setting(Settings.STEAM_AVATAR_URL) or "").strip(),
        }
    except Exception:
        return {"linked": False, "steamid64": "", "persona": "", "avatar": ""}


def logout_steam() -> dict:
    try:
        from sff.core.storage.settings import set_setting
        from sff.core.structs import Settings

        set_setting(Settings.STEAM_OPENID_ID, "")
        set_setting(Settings.STEAM_PERSONA, "")
        set_setting(Settings.STEAM_AVATAR_URL, "")
    except Exception as exc:
        logger.warning("Steam logout failed: %s", exc)
    return steam_account_dict()


def login_steam(parent=None) -> dict:
    """Open Steam OpenID in the system browser and wait for the localhost return."""
    captured: dict = {}
    error: list[str] = []

    class _Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            return

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path.rstrip("/") != "/steam_callback":
                self.send_response(404)
                self.end_headers()
                return
            qs = urllib.parse.parse_qs(parsed.query)
            captured["params"] = {k: v[0] for k, v in qs.items() if v}
            body = (
                f"<html><body style='font-family:sans-serif;background:#0b1220;color:#e8eef5;"
                f"display:flex;align-items:center;justify-content:center;height:100vh'>"
                f"<p>Signed in to {APP_NAME}. You can close this tab.</p></body></html>"
            ).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    httpd = HTTPServer(("127.0.0.1", 0), _Handler)
    httpd.timeout = 300
    port = httpd.server_address[1]
    realm = f"http://127.0.0.1:{port}"
    return_to = f"{realm}/steam_callback"
    query = urllib.parse.urlencode({
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.mode": "checkid_setup",
        "openid.return_to": return_to,
        "openid.realm": realm,
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
    })
    login_url = f"{_STEAM_OPENID}?{query}"

    def _serve():
        try:
            httpd.handle_request()
        except Exception as exc:
            error.append(str(exc))
        finally:
            try:
                httpd.server_close()
            except Exception:
                pass

    thread = threading.Thread(target=_serve, daemon=True)
    thread.start()

    opened = False
    try:
        from PyQt6.QtCore import QUrl
        from PyQt6.QtGui import QDesktopServices

        opened = QDesktopServices.openUrl(QUrl(login_url))
    except Exception:
        opened = False
    if not opened:
        import webbrowser

        webbrowser.open(login_url)

    _wait_qt(thread, timeout_ms=300_000)
    if error:
        return {"ok": False, "error": error[0], **steam_account_dict()}
    params = captured.get("params") or {}
    if not params:
        return {"ok": False, "error": "Steam login cancelled or timed out.", **steam_account_dict()}

    steamid = _verify_and_extract(params, return_to)
    if not steamid:
        return {"ok": False, "error": "Steam OpenID verification failed.", **steam_account_dict()}

    persona, avatar = _fetch_persona(steamid)
    try:
        from sff.core.storage.settings import set_setting
        from sff.core.structs import Settings

        set_setting(Settings.STEAM_OPENID_ID, steamid)
        set_setting(Settings.STEAM_PERSONA, persona)
        set_setting(Settings.STEAM_AVATAR_URL, avatar)
    except Exception as exc:
        logger.warning("Could not persist Steam account: %s", exc)
        return {"ok": False, "error": str(exc), **steam_account_dict()}

    account = steam_account_dict()
    account["ok"] = True
    return account


def _wait_qt(thread: threading.Thread, timeout_ms: int) -> None:
    try:
        from PyQt6.QtCore import QEventLoop, QTimer
        from PyQt6.QtWidgets import QApplication

        loop = QEventLoop()
        poll = QTimer()
        poll.setInterval(150)

        def _tick():
            if not thread.is_alive():
                loop.quit()

        poll.timeout.connect(_tick)
        poll.start()
        QTimer.singleShot(timeout_ms, loop.quit)
        app = QApplication.instance()
        if app is not None:
            loop.exec()
        else:
            thread.join(timeout_ms / 1000)
        poll.stop()
    except Exception:
        thread.join(timeout_ms / 1000)


def _verify_and_extract(params: dict, return_to: str) -> Optional[str]:
    mode = params.get("openid.mode", "")
    if mode != "id_res":
        return None
    claimed = params.get("openid.claimed_id", "")
    if not claimed.startswith(_CLAIMED_PREFIX):
        return None
    steamid = claimed[len(_CLAIMED_PREFIX):].strip("/")
    if not is_steamid64(steamid):
        return None
    if params.get("openid.return_to", "") != return_to:
        return None

    check = dict(params)
    check["openid.mode"] = "check_authentication"
    try:
        resp = httpx.post(
            _STEAM_OPENID,
            data=check,
            timeout=20,
            follow_redirects=True,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if resp.status_code != 200:
            return None
        if "is_valid:true" not in resp.text.replace(" ", "").lower() and "is_valid:true" not in resp.text.lower():
            # Steam returns "is_valid:true" on its own line
            lines = {line.strip().lower() for line in resp.text.splitlines()}
            if "is_valid:true" not in lines:
                return None
    except httpx.HTTPError as exc:
        logger.warning("Steam OpenID verify failed: %s", exc)
        return None
    return steamid


def _fetch_persona(steamid: str) -> tuple[str, str]:
    url = f"https://steamcommunity.com/profiles/{steamid}/?xml=1"
    try:
        resp = httpx.get(url, timeout=15, follow_redirects=True)
        if resp.status_code != 200 or not resp.content:
            return steamid, ""
        root = ET.fromstring(resp.content)
        name = (root.findtext(f"{_XML_NS}steamID") or root.findtext("steamID") or "").strip()
        avatar = (
            root.findtext(f"{_XML_NS}avatarMedium")
            or root.findtext("avatarMedium")
            or root.findtext(f"{_XML_NS}avatarIcon")
            or root.findtext("avatarIcon")
            or ""
        ).strip()
        return name or steamid, avatar
    except Exception as exc:
        logger.debug("Steam persona fetch failed: %s", exc)
        return steamid, ""
