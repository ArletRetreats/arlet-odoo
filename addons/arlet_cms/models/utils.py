def split_lines(text):
    """Split a multi-line Odoo Text field into a list of non-empty strings.

    Odoo Text fields return False when empty, so we guard against that.
    Used for array-type CMS fields (paragraphs, footer, list items, etc.)
    where admins enter one item per line.
    """
    if not text:
        return []
    return [line.strip() for line in str(text).split('\n') if line.strip()]
