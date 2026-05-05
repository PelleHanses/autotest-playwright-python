# Mouse Actions

Actions for clicking elements on the page.

---

## `click`

**Purpose:**  
Clicks an element.

**Parameters:**  
- `selector` (required) – CSS selector of the element  
- `timeout` (optional, default 10000) – wait until visible  

**Example YAML:**
```yaml
- click:
    selector: "#copyLinkBtn"
    info: "Click the copy link button"
```

