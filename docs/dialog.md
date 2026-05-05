# Dialog Actions

Actions for handling browser dialogs (alerts, confirms, prompts).

---

## `accept_dialog`

**Purpose:**  
Waits for the next dialog and accepts it.

**Parameters:**  
- `log_output` (optional, default False) – log the dialog text  

**Example YAML:**
```yaml
- accept_dialog:
    log_output: true
    info: "Accept any alert dialog that appears"
```

