#!/usr/bin/env python3
"""
Kör N instanser av ett YAML-test parallellt.

Varje tråd får sin egna sync_playwright()-instans (trådssäkert).
Variabeln {{user_index}} ersätts med 1..N i steps.

Exempel:
    python parallel_runner.py tests/prod/lobby_load_test.yml --users 20 --headless
    python parallel_runner.py tests/prod/lobby_load_test.yml --users 5 --ramp-delay 2
"""

import argparse
import copy
import sys
import time
import yaml
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Lägg till app/ i sökvägen så att runner, metric etc. hittas
sys.path.insert(0, str(Path(__file__).parent))

from runner import run_test
from logger import setup_logger
from metric import write_test_metric

logger = setup_logger()


def replace_user_index(obj, index: int):
    """Rekursivt ersätter {{user_index}} med aktuellt index."""
    if isinstance(obj, str):
        return obj.replace("{{user_index}}", str(index))
    if isinstance(obj, list):
        return [replace_user_index(i, index) for i in obj]
    if isinstance(obj, dict):
        return {k: replace_user_index(v, index) for k, v in obj.items()}
    return obj


def run_one(base_test: dict, user_index: int, browser: str, headless: bool) -> tuple[int, int, float]:
    """Kör ett test för en specifik användare, returnerar (user_index, exit_code, duration_ms)."""
    test = replace_user_index(copy.deepcopy(base_test), user_index)
    test["name"] = f"{base_test['name']}_user{user_index:03d}"

    logger.info(f"[START] user {user_index:03d} → {test['name']}")
    start = time.time()
    exit_code = run_test(test, browser, headless)
    duration_ms = int((time.time() - start) * 1000)
    status = "OK" if exit_code == 0 else "FAIL"
    logger.info(f"[{status}] user {user_index:03d} efter {duration_ms} ms")
    return user_index, exit_code, duration_ms


def main():
    parser = argparse.ArgumentParser(description="Parallel Playwright runner")
    parser.add_argument("testfile", help="YAML-testfil")
    parser.add_argument(
        "--browser",
        choices=["chromium", "firefox", "safari"],
        default="chromium",
    )
    parser.add_argument("--headless", action="store_true", help="Kör headless")
    parser.add_argument(
        "--users",
        type=int,
        default=5,
        help="Antal parallella användare (default: 5)",
    )
    parser.add_argument(
        "--ramp-delay",
        type=float,
        default=0.0,
        metavar="SEKUNDER",
        help="Fördröjning i sekunder mellan varje användarstart (ramp-up, default: 0)",
    )
    args = parser.parse_args()

    testfile = Path(args.testfile)
    if not testfile.exists():
        raise FileNotFoundError(f"Testfil saknas: {testfile}")

    with testfile.open() as f:
        tests = yaml.safe_load(f)

    if not tests:
        raise ValueError("Testfilen är tom eller ogiltig.")

    base_test = tests[0]
    logger.info(
        f"Startar {args.users} parallella instanser av '{base_test['name']}' "
        f"(browser={args.browser}, headless={args.headless}, ramp={args.ramp_delay}s)"
    )

    total = passed = failed = 0
    futures = {}

    with ThreadPoolExecutor(max_workers=args.users) as executor:
        for i in range(1, args.users + 1):
            future = executor.submit(run_one, base_test, i, args.browser, args.headless)
            futures[future] = i
            if args.ramp_delay > 0 and i < args.users:
                time.sleep(args.ramp_delay)

        for future in as_completed(futures):
            total += 1
            try:
                user_index, exit_code, duration_ms = future.result()
            except Exception as e:
                user_index = futures[future]
                exit_code = 1
                duration_ms = 0
                logger.error(f"[EXCEPTION] user {user_index:03d}: {e}")

            if exit_code == 0:
                passed += 1
            else:
                failed += 1

            write_test_metric(
                test_name=f"{base_test['name']}_user{user_index:03d}",
                browser=args.browser,
                success=exit_code,
                duration_ms=duration_ms,
            )

    print("\n=== PARALLEL TEST SUMMARY ===")
    print(f"Användare (trådar) : {args.users}")
    print(f"Total              : {total}")
    print(f"Passed             : {passed}")
    print(f"Failed             : {failed}")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
