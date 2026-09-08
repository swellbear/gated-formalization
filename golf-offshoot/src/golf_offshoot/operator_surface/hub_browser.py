"""Reuse the hub tab that is already open instead of stacking a new one.

The hub is a single-page console. On restart the right move is to refresh the
window already showing it, not to hand the founder another Chrome tab. Every
re-exec used to call into the browser again, so a long session ended up with a
row of identical tabs.

Windows first, via ctypes; no new dependency. Anywhere else this reports "no
hub window found" and the caller decides whether to open one.

Two guards keep the keystroke honest:

* a candidate must match on **both** title and window class, so the console
  running ``python -m golf_offshoot shell`` is never mistaken for the browser;
* F5 is only sent once the target is genuinely in the foreground, so a refused
  activation cannot leak the key into whatever the founder is typing in.
"""

from __future__ import annotations

import os
import sys
from urllib.parse import urlparse

#: The hub page's <title>. Browsers append their own suffix (" - Google Chrome"),
#: so this is matched as a substring.
HUB_TITLE = "golf-offshoot operator shell"

#: Set to 1 to leave foreground windows alone and always fall back to the browser.
NO_FOCUS_ENV = "GOLF_OFFSHOOT_HUB_NO_FOCUS"

#: Top-level classes for the browsers that can actually be showing the hub.
#: Chrome, Edge, Brave and Vivaldi all report Chrome_WidgetWin_1.
_BROWSER_CLASSES = (
    "chrome_widgetwin_1",
    "chrome_widgetwin_0",
    "mozillawindowclass",
    "applicationframewindow",
    "ieframe",
)

#: Consoles and editors that can legitimately carry the hub command line — or this
#: very source file — in their title bar. Never send them a keystroke.
_DENY_CLASSES = (
    "consolewindowclass",
    "cascadia_hosting_window_class",
    "pseudoconsolewindow",
    "windows.ui.core.corewindow",
    "chrome_widgetwin_1_electron",
)

VK_F5 = 0x74
_KEYEVENTF_KEYUP = 0x0002
_SW_RESTORE = 9


def hub_window_hints(url: str) -> tuple[str, ...]:
    """Title fragments that identify the hub window for ``url``."""
    parsed = urlparse(url or "")
    netloc = (parsed.netloc or "").strip()
    hints = [HUB_TITLE.lower()]
    if netloc:
        hints.append(netloc.lower())
    return tuple(dict.fromkeys(hints))


def title_matches(title: str, hints: tuple[str, ...]) -> bool:
    lowered = str(title or "").lower()
    if not lowered:
        return False
    return any(hint in lowered for hint in hints if hint)


def is_browser_window(window_class: str) -> bool:
    """True only for a top-level browser frame. Consoles are refused outright."""
    lowered = str(window_class or "").strip().lower()
    if not lowered:
        return False
    if lowered in _DENY_CLASSES:
        return False
    return lowered in _BROWSER_CLASSES


def choose_hub_window(
    candidates: list[tuple[int, str, str]],
    hints: tuple[str, ...],
) -> int | None:
    """First visible browser window whose title carries a hub hint.

    ``candidates`` is ``(hwnd, title, window_class)``. Kept pure so the match
    rules are testable without a desktop.
    """
    for hwnd, title, window_class in candidates:
        if not hwnd:
            continue
        if not is_browser_window(window_class):
            continue
        if title_matches(title, hints):
            return int(hwnd)
    return None


def focus_disabled(environ: dict[str, str] | None = None) -> bool:
    env = os.environ if environ is None else environ
    return (env.get(NO_FOCUS_ENV) or "").strip() == "1"


def list_windows() -> list[tuple[int, str, str]]:
    """Visible top-level windows as ``(hwnd, title, class)``. ``[]`` off Windows."""
    if not sys.platform.startswith("win"):
        return []
    try:
        import ctypes
        from ctypes import wintypes
    except Exception:
        return []
    try:
        user32 = ctypes.WinDLL("user32", use_last_error=True)
    except OSError:
        return []

    found: list[tuple[int, str, str]] = []
    proc_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    def _collect(hwnd, _lparam):
        try:
            if not user32.IsWindowVisible(hwnd):
                return True
            length = user32.GetWindowTextLengthW(hwnd)
            if length <= 0:
                return True
            title_buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, title_buf, length + 1)
            class_buf = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, class_buf, 256)
            found.append((int(hwnd), title_buf.value, class_buf.value))
        except Exception:
            return True
        return True

    try:
        user32.EnumWindows(proc_type(_collect), 0)
    except Exception:
        return []
    return found


def activate_and_refresh(hwnd: int) -> bool:
    """Bring ``hwnd`` forward and press F5. False if it never took the foreground."""
    if not sys.platform.startswith("win"):
        return False
    try:
        import ctypes
    except Exception:
        return False
    try:
        user32 = ctypes.WinDLL("user32", use_last_error=True)
    except OSError:
        return False
    try:
        if user32.IsIconic(hwnd):
            user32.ShowWindow(hwnd, _SW_RESTORE)
        user32.SetForegroundWindow(hwnd)
        # Windows can refuse an unsolicited foreground change. Sending F5 to a
        # window that never came forward would type into the founder's other app.
        if int(user32.GetForegroundWindow() or 0) != int(hwnd):
            return False
        user32.keybd_event(VK_F5, 0, 0, 0)
        user32.keybd_event(VK_F5, 0, _KEYEVENTF_KEYUP, 0)
    except Exception:
        return False
    return True


def refresh_existing_hub_window(
    url: str,
    *,
    lister=None,
    refresher=None,
    environ: dict[str, str] | None = None,
) -> bool:
    """Refresh the hub window already on screen. False means "nothing to reuse"."""
    if focus_disabled(environ):
        return False
    windows = (lister or list_windows)()
    if not windows:
        return False
    hwnd = choose_hub_window(list(windows), hub_window_hints(url))
    if hwnd is None:
        return False
    return bool((refresher or activate_and_refresh)(hwnd))
