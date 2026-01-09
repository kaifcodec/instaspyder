import unicodedata

def sanitize_text(text):
    if not text:
        return ""
    # NFKC form converts "fancy" styles (bold, script, double-struck) to normal letters
    normalized = unicodedata.normalize('NFKC', text)
    # Remove accents (diacritics) like 'é' -> 'e'
    # 'NFD' and filter out non-spacing mark characters
    nfd_form = unicodedata.normalize('NFD', normalized)
    return "".join([c for c in nfd_form if not unicodedata.combining(c)])

