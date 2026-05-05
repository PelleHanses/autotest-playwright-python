# Jitsi Actions

Actions specific to controlling Jitsi video meeting toggles.

---

## `ensure_toggle_state`

**Purpose:**  
Ensures a toggle button is in the desired state (`on` or `off`).

**Parameters:**  
- `selector` (required) – CSS selector of the toggle button  
- `state` (required) – desired state: `on` or `off`  

**Example YAML:**
```yaml
- ensure_toggle_state:
    selector: ".tileview-toggle"
    state: "on"
    info: "Enable tile view in Jitsi"
```
