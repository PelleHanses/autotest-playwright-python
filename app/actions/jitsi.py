from playwright.sync_api import TimeoutError

def ensure_toggle_state(page, params, logger):
    """
    Säkerställer att en toggle-knapp hamnar i önskat läge.

    params:
      selector: CSS-selector till toolbox-button
      state: "on" | "off"
    """

    selector = params.get("selector")
    desired_state = params.get("state")

    if not selector or desired_state not in ("on", "off"):
        raise Exception("ensure_toggle_state kräver selector och state=on|off")

    el = page.locator(selector)
    el.wait_for(state="visible")

    aria_pressed = el.get_attribute("aria-pressed")
    if aria_pressed not in ("true", "false"):
        raise Exception(f"Element {selector} saknar giltig aria-pressed")

    is_on = aria_pressed == "true"
    want_on = desired_state == "on"

    if is_on != want_on:
        logger.info(
            f"Toggle mismatch ({'on' if is_on else 'off'} → {desired_state}), klickar"
        )
        el.click()

        expected_value = "true" if want_on else "false"

        # ✅ Python korrekt
        page.wait_for_function(
            """
            (arg) => {
                const [selector, value] = arg;
                const el = document.querySelector(selector);
                return el && el.getAttribute('aria-pressed') === value;
            }
            """,
            arg=[selector, expected_value],
            timeout=5000,
        )
    else:
        logger.info(f"Toggle redan i rätt läge ({desired_state}), ingen åtgärd")

