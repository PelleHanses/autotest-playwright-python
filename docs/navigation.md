
---
# Navigation Actions

Actions to navigate and check URLs.

---

## `goto`

**Purpose:**  
Navigate to a given URL.

**Parameters:**  
- `url` (required) – the URL to navigate to  

**Example YAML:**
```yaml
- goto:
    url: "https://pre.xxx.yyy/video/book/"
    info: "Navigate to booking page"
```

## `check_url`

**Purpose:**
Checks if the current URL matches the expected value.

**Parameters:**

expected_url (required) – the URL to match

match (optional, default startswith) – match type (startswith, contains, regex)

**Example YAML:**
```yaml
- check_url:
    expected_url: "pre.xxx.yyy/video/book/"
    match: contains
    info: "Verify we are on the booking page"

```
## `wait_for_url`

**Purpose:**
Waits until the current URL matches an expected value.

**Parameters:**

expected_url (required) – the URL to match

match (optional, default startswith) – match type (startswith, contains, regex)

timeout (optional, default 15000ms) – maximum wait

**Example YAML:**
```yaml
- wait_for_url:
    expected_url: "pre.xxx.yyy/video/book/"
    match: contains
    info: "Wait until the URL contains 'video/book'"
```
