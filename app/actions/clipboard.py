# actions/clipboard.py
import time
from playwright.sync_api import Page

def clear_clipboard(page: Page, logger=None):
    page.evaluate("navigator.clipboard.writeText('')")
    if logger:
        logger.info("Clipboard tömd")

def read_clipboard(page, params=None, logger=None, url_history=None):
    """
    Läser clipboard och returnerar innehållet.

    Väntar tills clipboard inte är tomt, upp till timeout.

    Params:
      - timeout: max väntetid i sekunder (default: 5)
      - poll_interval: hur ofta clipboard kontrolleras i sekunder (default: 0.2)
      - log_output: True/False, loggar clipboard-innehållet om True (default: True)
    """
    timeout = (params or {}).get("timeout", 5)
    poll_interval = (params or {}).get("poll_interval", 0.2)
    log_output = (params or {}).get("log_output", True)

    start = time.time()
    content = ""

    while time.time() - start < timeout:
        try:
            content = page.evaluate("navigator.clipboard.readText()")
        except Exception as e:
            # Om browsern inte tillåter clipboard-read just nu
            content = ""
        if content:
            break
        time.sleep(poll_interval)

    if log_output:
        if logger:
            if content:
                logger.info(f"Clipboard innehåller: {content}")
            else:
                logger.warning(f"Clipboard är tom efter {timeout}s väntan")
        else:
            print(f"Clipboard: {content or '[tom]'}")

    return content

