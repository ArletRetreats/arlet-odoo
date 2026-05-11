from odoo import models, fields


class ArletLocation(models.Model):
    _name = 'arlet.location'
    _description = 'Arlet Location'
    _inherit = ['arlet.translatable.mixin']

    name = fields.Char(string='Location Name', required=True,
                       help='Proper noun — not localised (e.g. "Château Lacrou")')
    country = fields.Char(string='Country Code', help='ISO code, e.g. "BE"')
    # EN base values
    subtitle = fields.Char(string='Subtitle')
    html = fields.Html(string='Description')
    image = fields.Char(string='Image URL')
    image_alt = fields.Char(string='Image Alt')
    image_position = fields.Selection(
        [('left', 'Left'), ('right', 'Right')],
        string='Image Position',
        default='right',
    )
    translation_ids = fields.One2many('arlet.location.translation', 'location_id', string='Translations')

    def to_api_dict(self, locale='en'):
        """Full dict — used inside ContentBlock of type 'location'."""
        return {
            'id': str(self.id),
            'name': self.name or '',
            'country': self.country or '',
            'subtitle': self._t('subtitle', locale),
            'html': self._t('html', locale),
            'image': self.image or '',
            'imageAlt': self.image_alt or '',
            'imagePosition': self.image_position or 'right',
        }

    def to_list_api_dict(self):
        """Minimal dict for the listLocations endpoint."""
        data = {'id': str(self.id), 'name': self.name or ''}
        if self.country:
            data['country'] = self.country
        return data


class ArletLocationTranslation(models.Model):
    _name = 'arlet.location.translation'
    _description = 'Location Translation'
    _inherit = ['arlet.base.translation']

    location_id = fields.Many2one('arlet.location', required=True, ondelete='cascade')
    subtitle = fields.Char(string='Subtitle')
    html = fields.Html(string='Description')

    _sql_constraints = [(
        'locale_location_unique', 'UNIQUE(location_id, locale_id)',
        'A translation for this locale already exists for this location.',
    )]
