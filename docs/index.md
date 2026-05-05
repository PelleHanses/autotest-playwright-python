# Playwright Test Actions Documentation

This documentation provides an overview of all available test actions in the project.  
Each action module is self-contained and can be used declaratively in YAML test files.  

---

## Actions Overview

| Action File | Description | Example |
|-------------|-------------|---------|
| **assertions.py** | Contains actions to assert text or URL on the page. Useful for verifying page content or navigation. | [assertions.md](assertions.md) |
| **clipboard.py** | Actions to read, clear, and assert clipboard content. Handles waiting for clipboard data as well. | [clipboard.md](clipboard.md) |
| **dialog.py** | Actions to handle JavaScript dialogs (alert, confirm, prompt). Supports logging dialog messages. | [dialog.md](dialog.md) |
| **input.py** | Actions to fill input fields and select radio buttons. Includes visibility checks. | [input.md](input.md) |
| **jitsi.py** | Actions to ensure toggle-buttons in Jitsi interface are set correctly (on/off). Waits for state changes. | [jitsi.md](jitsi.md) |
| **mouse.py** | Actions for mouse interactions, e.g., click elements with visibility checks. | [mouse.md](mouse.md) |
| **navigation.py** | Navigate to URLs or check current page URL. Includes basic URL validation helpers. | [navigation.md](navigation.md) |
| **url_matcher.py** | Utility to match URLs using `startswith`, `contains`, or regular expressions. | [url_matcher.md](url_matcher.md) |
| **wait.py** | Actions for waiting: elements, specific time, or until URL matches a condition. | [wait.md](wait.md) |

---

## Recommended Usage

- Include `info` on every step in YAML for self-documenting tests.  
- Use `foreach` for repetitive actions over multiple items (e.g., multiple radio buttons or test data).  
- Prefer `assert_clipboard_contains` for verifying dynamic HTML or generated content.  
- Combine `wait_for_element` and `wait_for_url` to ensure page readiness before assertions.  

---

### Example Snippet (YAML)

```yaml
- goto:
    url: "https://pre.xxx.yyy/video/book/"
    info: "Navigate to the book page"

- foreach:
    items:
      - meeting: StandardMeeting
        expect:
          - "Something"
          - "userInfo.displayName"
      - meeting: LobbyMeeting
        expect:
          - "Something"
          - "_lobbyx"
    steps:
      - select_radio:
          selector: "label.meeting-label:has(input[value='{{meeting}}'])"
          info: "Select the radio button '{{meeting}}'"

      - click:
          selector: "#copyLinkBtn"
          info: "Click the copy link button"

      - read_clipboard:
          timeout: 3
          poll_interval: 0.1
          log_output: true
          info: "Wait until clipboard has content"

      - assert_clipboard_contains:
          contains: "{{expect}}"
          info: "Verify clipboard content for '{{meeting}}'"
```
