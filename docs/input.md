
---

### `docs/input.md`

```markdown
# Input Actions

Actions for filling inputs and selecting radio buttons.

---

## `fill_input`

**Purpose:**  
Fills a text input field.

**Parameters:**  
- `selector` (required) – CSS selector of the input  
- `value` (required) – value to fill  
- `timeout` (optional, default 10000) – wait until visible in milliseconds  

**Example YAML:**
```yaml
- fill_input:
    selector: "#username"
    value: "john.doe"
    info: "Fill in the username field"
```

## `select_radio`
**Purpose:
Selects a radio button.

Parameters:

selector (required) – CSS selector of the radio button

timeout (optional, default 10000) – wait until attached

Example YAML:
```yaml
- select_radio:
    selector: "input[value='StandardMeeting']"
    info: "Select the StandardMeeting option"

```

