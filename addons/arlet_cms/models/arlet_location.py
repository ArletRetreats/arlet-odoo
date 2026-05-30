from odoo import models, fields, api
from .utils import slugify, WEB_BASE


class ArletLocation(models.Model):
    _name = 'arlet.location'
    _description = 'Arlet Location'
    _inherit = ['arlet.translatable.mixin']

    name = fields.Char(string='Location Name', required=True,
                       help='Proper noun — not localised (e.g. "Château Lacrou")')
    slug = fields.Char(
        string='Slug',
        compute='_compute_slug', store=True, readonly=True,
        help='Auto-generated from the Location Name.',
    )
    country = fields.Char(string='Country Code', help='ISO code, e.g. "BE"')
    # EN base values
    subtitle = fields.Char(string='Subtitle')
    html = fields.Html(string='Description')
    image = fields.Image(string='Image', max_width=0, max_height=0)
    image_alt = fields.Char(string='Image Alt')
    image_position = fields.Selection(
        [('left', 'Left'), ('right', 'Right')],
        string='Image Position',
        default='right',
    )
    # Detail page
    hero_bg = fields.Image(string='Hero BG', max_width=0, max_height=0)
    hero_bg_alt = fields.Char(string='Hero BG Alt')
    content_ids = fields.One2many('arlet.content.block', 'location_article_id', string='Content Blocks')
    translation_ids = fields.One2many('arlet.location.translation', 'location_id', string='Translations')

    _constraints = [
        models.Constraint('slug_unique', 'UNIQUE(slug)', 'A location with this slug already exists.'),
    ]

    @api.depends('name')
    def _compute_slug(self):
        for rec in self:
            rec.slug = slugify(rec.name or '')

    def to_api_dict(self, locale='en'):
        """Full dict — used inside ContentBlock of type 'location'."""
        return {
            'id': str(self.id),
            'slug': self.slug or '',
            'name': self.name or '',
            'country': self.country or '',
            'subtitle': self._t('subtitle', locale),
            'html': self._t('html', locale),
            'image': self._img_url('image'),
            'imageAlt': self.image_alt or '',
            'imagePosition': self.image_position or 'right',
        }

    def to_detail_api_dict(self, locale='en'):
        """Full dict for the location detail page endpoint."""
        data = self.to_api_dict(locale)
        data.update({
            'heroBg': self._img_url('hero_bg'),
            'heroBgAlt': self.hero_bg_alt or '',
            'content': [block.to_api_dict(locale) for block in self.content_ids],
        })
        return data

    def to_list_api_dict(self):
        """Minimal dict for the listLocations endpoint."""
        data = {'id': str(self.id), 'slug': self.slug or '', 'name': self.name or ''}
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

    _constraints = [
        models.Constraint('locale_location_unique', 'UNIQUE(location_id, locale_id)', 'A translation for this locale already exists for this location.'),
    ]
