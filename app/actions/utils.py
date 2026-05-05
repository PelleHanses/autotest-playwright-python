import time


def wait(params, logger):
    """
    Väntar ett givet antal millisekunder.

    params:
      duration: väntetid i ms (default: 5000)
    """
    duration_ms = params.get("duration", 5000)
    logger.info(f"[WAIT] Väntar {duration_ms} ms")
    time.sleep(duration_ms / 1000)
