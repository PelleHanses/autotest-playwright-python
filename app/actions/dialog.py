# actions/dialog.py

def accept_dialog(page, params=None, logger=None, url_history=None):
    """
    Väntar på nästa dialog (alert/confirm/prompt) och accepterar den.
    
    Params (valfritt):
      log_output: bool - om dialogens text ska skrivas ut i loggen (default: False)
    """
    log_output = False
    if params:
        log_output = params.get("log_output", False)

    if not page:
        raise ValueError("Parameter 'page' krävs för accept_dialog")

    handled = {"done": False}

    def handle_dialog(dialog):
        if log_output and logger:
            logger.info(f"Dialog text: {dialog.message}")
        dialog.accept()
        handled["done"] = True

    page.on("dialog", handle_dialog)

    # Vänta tills dialogen hanteras
    # Vi använder page.wait_for_timeout med små intervall i max 5 sekunder
    import time
    for _ in range(50):
        if handled["done"]:
            break
        time.sleep(0.1)
    else:
        raise RuntimeError("Ingen dialog dök upp inom timeout")

    # Ta bort event listener för att inte påverka senare steg
    page.off("dialog", handle_dialog)

