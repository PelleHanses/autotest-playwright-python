# Playwright YAML Test Runner
A modular test runner for browser automation using Playwright and YAML configuration files. Designed to execute browser steps without hardcoding logic, making it easy to add new tests and actions.

## Features
- Dynamically loads actions from the actions/ folder
- Supports Chromium, Firefox, and Safari
- Can run in headless or headed mode
- Color-coded terminal logging (INFO, WARNING, ERROR)
- URL assertions: startswith, contains, regex
- Waits for elements, fills input fields, clicks buttons, selects radio buttons, etc.
- Supports fake camera, microphone, and speaker for automated media testing
- Generates Prometheus-style metrics in metrics/test_metrics.prom
- Tracks total, passed, failed tests and prints a summary

## Flow Diagram
┌───────────────┐
│  runner.py    │
│  (main loop)  │
└───────┬───────┘
        ▼
┌───────────────┐
│  Load YAML    │
│ (tests/*.yml) │
└───────┬───────┘
        ▼
┌───────────────┐
│ Iterate over  │
│  steps        │
└───────┬───────┘
        ▼
┌───────────────┐
│ Dynamically   │
│ load actions  │
│ from actions/ │
└───────┬───────┘
        ▼
┌───────────────┐
│ Execute action│
│ (fill_input,  │
│ click_element,│
│ wait_for_url, │
│ select_radio) │
└───────────────┘

## Installation

Clone the repository:
```
git clone <repo-url>
cd <repo-folder>
```

Install required Python packages:
```
python3 -m pip install -r requirements.txt
```
Install Playwright browsers:
```
python3 -m playwright install
```
## Usage
```
./runner.py --file tests/prod/meet_login_guest.yaml --browser chromium --headless false
```

## CLI Parameters
| Parameter         | Description                                   |
| ----------------- | --------------------------------------------- |
| `--file` (`-f`)   | YAML file containing test cases (required)    |
| `--browser`       | chromium, firefox, safari (default: chromium) |
| `--headless`      | true or false (default: false)                |
| `--clear-metrics` | Clears the metrics file before running        |

## Test Summary

At the end of each run, the runner prints a summary both in CLI and log:
```
=== TEST SUMMARY ===
Total tests: 3
Passed: 2
Failed: 1
```
This allows immediate insight into test results.

## Creating a New Action

1. Create a Python file in actions/, e.g., actions/my_action.py.

2. Define the function with the following signature:
```
def my_action(page, params, logger, url_history=None):
    selector = params["selector"]
    logger.info(f"Doing something with {selector}")
    page.fill(selector, "text")
```

3. Add the action in your YAML test:
```
- my_action:
    selector: "#input-field"
  info: "Fills the input field"
```

4. The runner automatically loads all .py files in the actions/ folder.

## Example YAML Test File
```
- name: Jitsi-guest-full-login-flow
  steps:
    - goto:
        url: "https://jitsi-preprod.sgit.se/test_auto01"
      info: "Navigate to Jitsi"

    - wait:
        ms: 4000
      info: "Wait for 4 seconds"

    - wait_for_url:
        expected_url: "https://pre.xxx.yyy/video/login/login.php?/test_auto01?state="
        match: contains
      info: "Verify redirect to login page"

    - select_radio:
        selector: "input[name='userType'][value='guest']"
      info: "Select 'Guest' radio button"

    - fill_input:
        selector: "#name"
        value: " Guest"
      info: "Fill in name"

    - click_element:
        selector: "#submitBtn"
      info: "Click the submit button"
```

## Logging
- Console: ANSI-colored (INFO=white, WARNING=yellow, ERROR=red)
- File: Saved in log/test_YYYYMMDD_HHMMSS.log without colors
- Actions automatically receive a logger if the function includes the logger parameter.

## Metrics
- Generated in metrics/test_metrics.prom
- Includes total, passed, failed tests with Unix timestamp:
```
test_total 3 1735503268
test_passed 2 1735503268
test_failed 1 1735503268
```
- Can be cleared before a run:
```
./runner.py --file tests/test.yaml --clear-metrics
```

## Test Types
Our testing strategy distinguishes between three main types of tests: **Smoke**, **Regression**, and **Production (Prod) Monitoring**.
| Type           | Purpose                                                                           |
| -------------- | --------------------------------------------------------------------------------- |
| **Smoke**      | Quick checks for critical workflows, run frequently. Failures stop further tests. |
| **Regression** | Comprehensive tests for functional coverage, run in dev/preprod.                  |
| **Production** | Lightweight, read-only tests for live monitoring. Failures trigger alerts.        |

### Smoke Tests
- Quick, basic checks to ensure the system is up and running.
- Validate critical workflows with minimal steps.
- Run frequently during development and after deployments.
- Failures indicate immediate issues; no further tests are executed.

### Regression Tests
- Comprehensive tests to ensure existing functionality has not been broken by new changes.
- Cover multiple scenarios, including previously reported bugs.
- Can modify data or perform deeper interactions.
- Typically run in development or pre-production environments.
- Failures indicate functional regressions that need to be fixed before release.

### Production (Prod) Monitoring Tests
- Lightweight, read-only tests that verify system availability in the live environment.
- Focus on essential endpoints and pages without changing data.
- Run frequently (e.g., every few minutes) to detect downtime or major issues.
- Failures trigger alerts for the operations team but do not indicate regressions in functionality.

## API (Flask)
A simple API allows remote triggering of tests.

### Start API
```
python3 -m venv /opt/test-runner/venv
source /opt/test-runner/venv/bin/activate
pip install flask
python run_tests_api.py
```
### API Request
```
curl -X POST http://localhost:8084/run_test \
  -H "Content-Type: application/json" \
  -d '{"test": "meet_login_guest_preprod.yaml"}'
```
### API Response
```
{
  "status": "started",
  "test": "meet_login_guest_preprod.yaml"
}
```
- Respects MAX_CONCURRENT_TESTS
- Automatically runs tests in a Podman container

### Start API-scriptet automatic at systemd
Put auto start in systemd
```
sudo vim /etc/systemd/system/test-runner-api.service
```
Put in the script from test-runner-api.service

## Docker / Podman
### Build
```
docker build -f Dockerfile -t playwright_python:1.0.0 .
podman build -f Dockerfile -t playwright_python:1.0.0 .
```
### Run test
```
docker compose run --rm guest_preprod
podman-compose run --rm guest_preprod
```
### Run test many guests to Jitsi
Here we override runner.py
```
sudo -xxxx podman-compose run --rm --entrypoint "python parallel_runner.py" playwright /work/tests/prod/lobby_load_test.yml --users 40 --headless --ramp-delay 5
```
Run with docker
```
docker compose run --rm --entrypoint "python parallel_runner.py" playwright /work/tests/prod/lobby_load_test.yml --users 40 --headless --ramp-delay 5
```

## License
MIT License © Pelle Hanses
```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
```


