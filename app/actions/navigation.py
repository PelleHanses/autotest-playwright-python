import re

# --------------------------------------------------
# Navigera till URL
# --------------------------------------------------
def goto(page, params, logger=None, url_history=None):
    """
    Navigera till angiven URL.
    params: {"url": "..."}
    """
    url = params.get("url")
    if not url:
        raise ValueError("Parameter 'url' saknas för goto-action")

    wait_until = params.get("wait_until", "domcontentloaded")
    timeout = params.get("timeout", 60000)

    if logger:
        logger.info(f"Navigating to: {url}")

    #page.goto(url)
    page.goto(url, wait_until=wait_until, timeout=timeout)

# --------------------------------------------------
# Kontrollera URL
# --------------------------------------------------
def check_url(page, params, logger=None, url_history=None):
    """
    Kontrollera att aktuell URL matchar expected_url enligt match-typ.
    params: {"expected_url": "...", "match": "startswith|contains|regex"}
    """
    expected_url = params.get("expected_url")
    match_type = params.get("match", "startswith")
    current_url = page.url
    url_history = url_history or []

    matched = False
    if match_type == "startswith":
        matched = current_url.startswith(expected_url)
    elif match_type == "contains":
        matched = expected_url in current_url
    elif match_type == "regex":
        matched = re.match(expected_url, current_url) is not None
    else:
        if logger:
            logger.warning(f"Unknown match type '{match_type}', defaulting to startswith")
        matched = current_url.startswith(expected_url)

    if not matched:
        if logger:
            logger.error(
                f"URL check failed ({match_type})\n"
                f"  Expected: {expected_url}\n"
                f"  Current : {current_url}\n"
                f"  URL history: {url_history}"
            )
    else:
        if logger:
            logger.info(f"URL check OK ({match_type}): {current_url}")

    return matched
