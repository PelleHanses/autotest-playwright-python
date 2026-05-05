# URL Matcher Utility

Helper functions to match URLs for assertions and waits.

---

## `match_url`

**Purpose:**  
Checks whether the current URL matches the expected URL according to the specified match type.

**Parameters:**  
- `current_url` – current page URL  
- `expected` – expected URL string  
- `match_type` – type of match:  
  - `startswith` – checks if current URL starts with expected  
  - `contains` – checks if current URL contains expected  
  - `regex` – checks if current URL matches regular expression  

**Returns:**  
- `True` if the URL matches  
- `False` if the URL does not match  

**Example usage in Python:**
```python
from actions.url_matcher import match_url

current_url = "https://pre.xxx.yyy/video/book/index.php"
expected = "video/book"
match_type = "contains"

if match_url(current_url, expected, match_type):
    print("URL matches")
else:
    print("URL mismatch")
```

