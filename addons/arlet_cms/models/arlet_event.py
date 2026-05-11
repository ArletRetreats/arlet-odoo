from odoo import models, fields


class ArletEvent(models.Model):
    _name = 'arlet.event'
    _description = 'Arlet Event'
    _order = 'start_date asc'
    _inherit = ['arlet.translatable.mixin']

    name = fields.Char(string='Internal Name', required=True)
    category = fields.Selection([
        ('retreat', 'Retreat'),
        ('dinner', 'Dinner'),
        ('workshop', 'Workshop'),
        ('experience', 'Experience'),
    ], required=True)
    # EN base values (used as fallback when translation is missing)
    title = fields.Char(string='Title', required=True)
    location = fields.Char(string='Location')
    description = fields.Text(string='Description')
    image = fields.Char(string='Image URL')
    slug = fields.Char(string='Slug', default='')
    coming_soon = fields.Boolean(string='Coming Soon', default=False)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    program_ids = fields.One2many('arlet.event.program.day', 'event_id', string='Program')
    translation_ids = fields.One2many('arlet.event.translation', 'event_id', string='Translations')

    def to_api_dict(self, locale='en'):
        data = {
            'id': str(self.id),
            'category': self.category.capitalize() if self.category else '',
            'title': self._t('title', locale),
            'startDate': self.start_date.isoformat() if self.start_date else '',
            'endDate': self.end_date.isoformat() if self.end_date else '',
            'location': self._t('location', locale),
            'description': self._t('description', locale),
            'image': self.image or '',
            'slug': self.slug or '',
            'comingSoon': self.coming_soon,
        }
        if self.program_ids:
            data['program'] = [day.to_api_dict(locale) for day in self.program_ids]
        return data


class ArletEventTranslation(models.Model):
    _name = 'arlet.event.translation'
    _description = 'Event Translation'
    _inherit = ['arlet.base.translation']

    event_id = fields.Many2one('arlet.event', required=True, ondelete='cascade')
    title = fields.Char(string='Title')
    location = fields.Char(string='Location')
    description = fields.Text(string='Description')

    _sql_constraints = [(
        'locale_event_unique', 'UNIQUE(event_id, locale_id)',
        'A translation for this locale already exists for this event.',
    )]


class ArletEventProgramDay(models.Model):
    _name = 'arlet.event.program.day'
    _description = 'Event Program Day'
    _order = 'sequence asc'
    _rec_name = 'date_label'
    _inherit = ['arlet.translatable.mixin']

    event_id = fields.Many2one('arlet.event', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    date_label = fields.Char(
        string='Date Label', required=True,
        help='Human-readable, e.g. "Friday, July 17th 2025"',
    )
    theme = fields.Char(string='Day Theme', help='e.g. "Gentle Arrival"')
    slot_ids = fields.One2many('arlet.event.program.slot', 'day_id', string='Slots')
    translation_ids = fields.One2many(
        'arlet.event.program.day.translation', 'day_id', string='Translations',
    )

    def to_api_dict(self, locale='en'):
        data = {
            'date': self._t('date_label', locale),
            'slots': [slot.to_api_dict(locale) for slot in self.slot_ids],
        }
        theme = self._t('theme', locale)
        if theme:
            data['theme'] = theme
        return data


class ArletEventProgramDayTranslation(models.Model):
    _name = 'arlet.event.program.day.translation'
    _description = 'Program Day Translation'
    _inherit = ['arlet.base.translation']

    day_id = fields.Many2one('arlet.event.program.day', required=True, ondelete='cascade')
    date_label = fields.Char(string='Date Label')
    theme = fields.Char(string='Day Theme')

    _sql_constraints = [(
        'locale_day_unique', 'UNIQUE(day_id, locale_id)',
        'A translation for this locale already exists for this day.',
    )]


class ArletEventProgramSlot(models.Model):
    _name = 'arlet.event.program.slot'
    _description = 'Event Program Slot'
    _order = 'sequence asc'
    _rec_name = 'start_at'
    _inherit = ['arlet.translatable.mixin']

    day_id = fields.Many2one('arlet.event.program.day', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    start_at = fields.Char(string='Start At', required=True, help='e.g. "7.45 AM"')
    end_at = fields.Char(string='End At', help='e.g. "10.00 AM". Leave empty for single-point.')
    activity = fields.Char(string='Activity', required=True)
    translation_ids = fields.One2many(
        'arlet.event.program.slot.translation', 'slot_id', string='Translations',
    )

    def to_api_dict(self, locale='en'):
        data = {
            'startAt': self.start_at or '',
            'activity': self._t('activity', locale),
        }
        if self.end_at:
            data['endAt'] = self.end_at
        return data


class ArletEventProgramSlotTranslation(models.Model):
    _name = 'arlet.event.program.slot.translation'
    _description = 'Program Slot Translation'
    _inherit = ['arlet.base.translation']

    slot_id = fields.Many2one('arlet.event.program.slot', required=True, ondelete='cascade')
    activity = fields.Char(string='Activity')

    _sql_constraints = [(
        'locale_slot_unique', 'UNIQUE(slot_id, locale_id)',
        'A translation for this locale already exists for this slot.',
    )]
