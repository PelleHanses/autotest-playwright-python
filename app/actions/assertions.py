from actions.url_matcher import match_url

def search_text(page, params, logger=None, url_history=None):
    text = params.get("text")
    if not text:
        raise ValueError("Parameter 'text' saknas för search_text")
    if logger:
        logger.info(f"Searching for text: {text}")
    if text not in page.content():
        raise AssertionError(f"Text not found: {text}")

def assert_text(page, params, logger=None, url_history=None):
    text = params.get("text")
    if not text:
        raise ValueError("Parameter 'text' saknas för assert_text")
    if logger:
        logger.info(f"Asserting text: {text}")
    if text not in page.content():
        raise AssertionError(f"Text '{text}' not found on page")

def assert_url(page, params, logger=None, url_history=None):
    expected = params.get("expected_url")
    match_type = params.get("match", "startswith")
    if not expected:
        raise ValueError("Parameter 'expected_url' saknas för assert_url")

    current = page.url
    if logger:
        logger.info(f"Assert URL ({match_type}): expected='{expected}', current='{current}'")

    if not match_url(current, expected, match_type):
        history_str = " -> ".join(url_history) if url_history else "N/A"
        raise AssertionError(
            f"\nURL mismatch\n"
            f"  match    : {match_type}\n"
            f"  expected : {expected}\n"
            f"  current  : {current}\n"
            f"  history  : {history_str}"
        )

# actions/clipboard.py
def assert_clipboard_contains(page, params, logger=None, url_history=None):
    """
    Kontrollerar att clipboard innehåller angivna strängar.
    Params:
      contains: str | list[str]
      timeout: ms (optional)
      ignore_whitespace: bool (optional) – tar bort radbrytningar
    """

    contains = params.get("contains")

    timeout = params.get("timeout", 5000)
    ignore_whitespace = params.get("ignore_whitespace", True)

    if not contains:
        raise ValueError("Parameter 'contains' krävs för assert_clipboard_contains")

    if isinstance(contains, str):
        contains = [contains]

    if logger:
        logger.info("Läser clipboard-innehåll")

    try:
        clipboard_text = page.evaluate("""() => navigator.clipboard.readText()""")
    except Exception as e:
        raise AssertionError(f"Kunde inte läsa clipboard: {e}")

    if ignore_whitespace:
        clipboard_text = clipboard_text.replace("\n", "").replace("\r", "").strip()

    if logger:
        logger.debug(f"Clipboard innehåll:\n{clipboard_text}")

    for expected in contains:
        if expected not in clipboard_text:
            raise AssertionError(
                f"Förväntad sträng saknas i clipboard: '{expected}'"
            )

    if logger:
        logger.info("Clipboard verifierat OK")

