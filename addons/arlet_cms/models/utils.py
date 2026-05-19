import os
import re
import unicodedata

WEB_BASE = os.environ.get('ARLET_WEB_BASE', 'http://localhost:3000')
ODOO_BASE = os.environ.get('ARLET_ODOO_BASE', 'http://localhost:8069')


def slugify(text):
    """Return a URL-safe, lowercase, hyphen-separated slug derived from *text*.

    Example: "Château Lacrou" -> "chateau-lacrou"
    """
    if not text:
        return ''
    # Decompose accents then drop non-ASCII bytes
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def split_lines(text):
    """Split a multi-line Odoo Text field into a list of non-empty strings.

    Odoo Text fields return False when empty, so we guard against that.
    Used for array-type CMS fields (paragraphs, footer, list items, etc.)
    where admins enter one item per line.
    """
    if not text:
        return []
    return [line.strip() for line in str(text).split('\n') if line.strip()]
