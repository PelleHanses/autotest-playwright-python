# Clipboard Actions

This module provides actions for interacting with the browser clipboard.

---

## `clear_clipboard`

**Purpose:**  
Clears the system clipboard.

**Parameters:**  
- None

**Example YAML:**
```yaml
- clear_clipboard:
    info: "Clearing clipboard before next test"

## `read_clipboard`

**Purpose:**
Reads the current text from the clipboard. Waits until the clipboard is not empty, up to a timeout.

**Parameters:**

timeout (optional, default 5) – maximum wait time in seconds

poll_interval (optional, default 0.2) – how often to check the clipboard

log_output (optional, default True) – if True, logs the clipboard contents

**Example YAML:**
```yaml
- read_clipboard:
    timeout: 3
    poll_interval: 0.1
    log_output: true
    info: "Waiting for clipboard to fill"
```
## `assert_clipboard_contains`
**Purpose:**
Asserts that the clipboard contains one or more expected strings.

**Parameters:**

contains (string or list of strings, required) – values expected in clipboard

timeout (optional, ignored for now)

ignore_whitespace (optional, default True) – removes line breaks before assertion

**Example YAML:**
```yaml
- assert_clipboard_contains:
    contains:
      - "Something"
      - "userInfo.displayName"
    info: "Verify that correct HTML has been copied to clipboard"

```


