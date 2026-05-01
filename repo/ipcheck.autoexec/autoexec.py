import urllib.request
import json

TOKEN = "87e00bca0b8e3f"

# =========================
# SAFE KODI DETECTION
# =========================
try:
    import xbmc
    import xbmcgui
    KODI_AVAILABLE = True
except ImportError:
    xbmc = None
    xbmcgui = None
    KODI_AVAILABLE = False


# =========================
# FETCH IP INFO
# =========================
def fetch_ip_info():
    url = f"https://ipinfo.io/json?token={TOKEN}"
    with urllib.request.urlopen(url, timeout=5) as response:
        data = json.load(response)

    ip = data.get("ip", "Unknown IP")
    org = data.get("org", "Unknown ISP")

    if org.startswith("AS"):
        org = org.split(" ", 1)[-1]

    return org, ip


# =========================
# OUTPUT HANDLERS
# =========================
def show_notification(title, message, warning=False):
    """
    Works only in Kodi. Safe fallback in Windows.
    """
    if KODI_AVAILABLE:
        icon = xbmcgui.NOTIFICATION_WARNING if warning else xbmcgui.NOTIFICATION_INFO

        xbmcgui.Dialog().notification(
            heading=title,
            message=message,
            icon=icon,
            time=12000
        )
    else:
        # Windows debug fallback
        prefix = "⚠️ " if warning else ""
        print(f"{prefix}{title}: {message}")


# =========================
# VPN RULE
# =========================
def is_unprotected_isp(isp):
    return isp.strip().lower() == "plusnet"


# =========================
# MAIN
# =========================
def main():
    isp, ip = fetch_ip_info()
    message = f"{isp}: {ip}"

    if is_unprotected_isp(isp):
        show_notification(
            "VPN REQUIRED",
            f"Public ISP detected: {message}\nEnable VPN immediately.",
            warning=True
        )
    else:
        show_notification(
            "Network Info",
            message,
            warning=False
        )


if __name__ == "__main__":
    main()