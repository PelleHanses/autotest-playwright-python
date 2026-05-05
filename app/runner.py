#!/usr/bin/env python3

import argparse
import yaml
from pathlib import Path
import importlib
import inspect

from playwright.sync_api import sync_playwright
from logger import setup_logger
from metric import write_test_metric
import time
import json
import copy

logger = setup_logger()

def resolve_templates(obj, variables):
    if isinstance(obj, str):
        for k, v in variables.items():
            if isinstance(obj, str):
                for k, v in variables.items():
                    placeholder = f"{{{{{k}}}}}"
                    if placeholder in obj:
                        if isinstance(v, (str, int, float)):
                            obj = obj.replace(placeholder, str(v))
                        else:
                            # Om hela strängen är exakt "{{var}}", ersätt med objektet
                            if obj.strip() == placeholder:
                                return v
        return obj

    if isinstance(obj, list):
        return [resolve_templates(i, variables) for i in obj]

    if isinstance(obj, dict):
        return {k: resolve_templates(v, variables) for k, v in obj.items()}

    return obj

# --- Dynamically load all actions from actions/ ---
actions = {}
actions_dir = Path("actions")

for py_file in sorted(actions_dir.glob("*.py")):
    module_name = py_file.stem
    module = importlib.import_module(f"actions.{module_name}")
    for name, func in inspect.getmembers(module, inspect.isfunction):
        actions[name] = func


def log_error_step(step_name, exception, current_url, url_history, expected_url=None):
    logger.error(
        "\n=== STEP FAILED ===\n"
        f"Step         : {step_name}\n"
        f"Exception    : {exception}\n"
        f"Expected URL : {expected_url or 'N/A'}\n"
        f"Current URL  : {current_url}\n"
        "URL history  :\n"
        + "\n".join(f"  - {u}" for u in url_history) +
        "\n=================="
    )

def run_steps(steps, page, logger, url_history, parent_info=None):
    """
    Kör steg rekursivt.

    parent_info: används för att bygga fullständig steg-beskrivning i nested foreach
    """
    for step in steps:
        # --- Hämta info (beskrivning) ---
        step_info = step.get("info", "")
        full_info = f"{parent_info} > {step_info}" if parent_info else step_info

        try:
            # --- FOREACH ---
            if "foreach" in step:
                loop = step["foreach"]
                items = loop.get("items", [])
                inner_steps = loop.get("steps", [])

                if not isinstance(items, list):
                    raise ValueError("foreach.items måste vara en lista")

                for item in items:
                    logger.info(f"[FOREACH] {json.dumps(item, ensure_ascii=False)}")
                    resolved_steps = resolve_templates(copy.deepcopy(inner_steps), item)
                    # Rekursivt med full_info
                    run_steps(resolved_steps, page, logger, url_history, parent_info=full_info)

                continue

            # --- VANLIGT STEG ---
            action_keys = [k for k in step.keys() if k != "info"]
            if not action_keys:
                logger.warning(f"Inget action hittades i steg: {step_info}")
                continue

            action_name = action_keys[0]
            action_params = step.get(action_name, {})

            if action_name not in actions:
                logger.warning(f"Action '{action_name}' inte hittad i steg: {full_info}")
                continue

            action_func = actions[action_name]

            sig = inspect.signature(action_func)
            kwargs = {}
            if "page" in sig.parameters:
                kwargs["page"] = page
            if "params" in sig.parameters:
                kwargs["params"] = resolve_templates(action_params or {}, variables={})
            if "logger" in sig.parameters:
                kwargs["logger"] = logger
            if "url_history" in sig.parameters:
                kwargs["url_history"] = url_history

            # --- Kör steget ---
            logger.info(f"[STEP START] {full_info} ({action_name})")
            action_func(**kwargs)
            logger.info(f"[STEP OK] {full_info} ({action_name})")

        except Exception as e:
            logger.error(f"[STEP FAIL] {full_info} ({action_name}): {e}")
            raise

def run_test(test, browser_name, headless):
    logger.info(f"Running test '{test['name']}' on {browser_name}")
    success = 1
    url_history = []

    with sync_playwright() as p:
        if browser_name.lower() == "chromium":
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    "--use-fake-ui-for-media-stream",
                    "--use-fake-device-for-media-stream",
                    "--use-file-for-fake-video-capture=test.y4m",
                ],
            )
        elif browser_name.lower() == "firefox":
            browser = p.firefox.launch(headless=headless)
        else:
            browser = p.webkit.launch(headless=headless)

        context = browser.new_context(
            permissions=[
                "camera",
                "microphone",
                "clipboard-read",
                "clipboard-write",
            ]
        )
        page = context.new_page()


        page.on(
            "framenavigated",
            lambda frame: url_history.append(frame.url)
            if frame == page.main_frame else None
        )

        try:
            run_steps(test.get("steps", []), page, logger, url_history)
            return 0            # 0 = OK
        except Exception as e:
            log_error_step(
                "foreach",
                e,
                page.url,
                url_history,
            )
            return 1            # 1 = Fail
        finally:
            browser.close()

def main():
    parser = argparse.ArgumentParser(description="Playwright test runner")
    parser.add_argument("testfile", help="YAML test file")
    parser.add_argument("--browser", choices=["chromium", "firefox", "safari"], default="chromium")
    parser.add_argument("--headless", action="store_true")

    args = parser.parse_args()

    testfile = Path(args.testfile)
    if not testfile.exists():
        raise FileNotFoundError(testfile)

    with testfile.open() as f:
        tests = yaml.safe_load(f)

    # --- Init räknare ---
    total = 0
    passed = 0
    failed = 0

    for test in tests:
        total += 1
        start_ts = time.time()
        exit_code = run_test(test, args.browser, args.headless)
        duration_ms = int((time.time() - start_ts) * 1000)

        # Uppdatera pass/fail
        if exit_code == 0:
            passed += 1
        else:
            failed += 1

        write_test_metric(
            test_name=test["name"],
            browser=args.browser,
            success=exit_code,        # 0=OK, 1=FAIL
            duration_ms=duration_ms,
        )

    logger.info("=== TEST SUMMARY ===")
    logger.info(f"Total tests: {total}")
    logger.info(f"Passed: {passed}")
    logger.info(f"Failed: {failed}")

    # --- Summering i CLI och logg ---
    print("")
    print("\n=== TEST SUMMARY ===")
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()

