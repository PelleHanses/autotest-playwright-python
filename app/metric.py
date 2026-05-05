from pathlib import Path
import time
import re
import os

# Ska matcha det Alloy skrapar 
METRIC_DIR = Path(os.getenv("METRIC_DIR", "/work/metrics"))
METRIC_DIR.mkdir(parents=True, exist_ok=True)


def _sanitize_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", name)


def write_test_metric(
    test_name: str,
    browser: str,
    success: int,
    duration_ms: int,
):
    """
    Skriver Prometheus-metrics för ETT test (atomiskt).
    """

    safe_name = _sanitize_name(test_name)
    safe_browser = browser.lower()

    metric_file = METRIC_DIR / f"autotest_{safe_name}_{safe_browser}.prom"
    tmp_file = metric_file.with_suffix(".tmp")

    status_value = success
    #0 if success else 1
    timestamp_ms = int(time.time() * 1000)

    content = f"""# HELP autotest Resultat av Playwright-test (0=OK, 1=ERROR)
# TYPE autotest gauge
autotest{{app_name="playwright",test="{test_name}",browser="{safe_browser}"}} {status_value}

# HELP autotest_timestamp Tidpunkt när testet kördes (epoch ms)
# TYPE autotest_timestamp gauge
autotest_timestamp{{app_name="playwright",test="{test_name}",browser="{safe_browser}"}} {timestamp_ms}

# HELP autotest_duration_ms Total körtid för testet i millisekunder
# TYPE autotest_duration_ms gauge
autotest_duration_ms{{app_name="playwright",test="{test_name}",browser="{safe_browser}"}} {duration_ms}
"""

    tmp_file.write_text(content)
    tmp_file.replace(metric_file)
