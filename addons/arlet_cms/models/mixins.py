from odoo import models, fields


class ArletTranslatableMixin(models.AbstractModel):
    """
    Provides _t(field_name, locale) helper.
    Falls back to the base (EN) value when a translation is missing.

    Concrete models must declare their own `translation_ids` One2many
    pointing to a model that inherits `arlet.base.translation`.
    """
    _name = 'arlet.translatable.mixin'

    def _t(self, field_name, locale):
        """Return field value for locale, falling back to the EN base value."""
        if locale == 'en':
            val = getattr(self, field_name, '') or ''
        else:
            trans = self.translation_ids.filtered(lambda t: t.locale.code == locale)
            val = getattr(trans[0], field_name, None) if trans else None
            val = val or getattr(self, field_name, '') or ''
        # Cast Markup / False / None to plain str for JSON serialisation
        return str(val) if val else ''


class ArletBaseTranslation(models.AbstractModel):
    """
    Abstract base for every *Translation model.
    Provides the shared `locale` Selection.

    To add a new language, add an entry to the Selection here —
    all translation models inherit it automatically.
    """
    _name = 'arlet.base.translation'
    _rec_name = 'locale'

    locale = fields.Many2one(
        'arlet.locale', required=True, string='Language', ondelete='restrict',
    )
