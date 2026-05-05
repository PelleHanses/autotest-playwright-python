# Wait Actions

Actions to wait for elements, time, or URL changes.

---

## `wait_for_element`

**Purpose:**  
Waits until a DOM element is present on the page.

**Parameters:**  
- `selector` (required) – CSS selector of the element  
- `timeout` (optional, default 10000ms) – maximum wait in milliseconds  

**Example YAML:**
```yaml
- wait_for_element:
    selector: "#copyLinkBtn"
    timeout: 5000
    info: "Wait for the copy link button to appear"
```

## `wait`

**Purpose:**
Pauses execution for a given amount of time.

**Parameters:**

ms (optional, default 1000) – milliseconds to wait

**Example YAML:**
```yaml
- wait:
    ms: 2000
    info: "Wait 2 seconds before continuing"
```

## `wait_for_url`

**Purpose:**
Waits until the current URL matches an expected value.

**Parameters:**

expected_url (required) – URL to wait for

match (optional, default startswith) – type of match (startswith, contains, regex)

timeout (optional, default 15000ms) – maximum wait in milliseconds

**Example YAML:**
```yaml
- wait_for_url:
    expected_url: "pre.xxx.yyy/video/book/"
    match: contains
    timeout: 10000
    info: "Wait until the page URL contains 'video/book'"
```
