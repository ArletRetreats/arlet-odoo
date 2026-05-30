from odoo import models, fields, api
from .utils import slugify


class ArletEventCategory(models.Model):
    _name = 'arlet.event.category'
    _description = 'Arlet Event Category'
    _order = 'sequence asc, name asc'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    key = fields.Char(
        string='Key',
        compute='_compute_key', store=True, readonly=True,
        help='Auto-generated lowercase key derived from the Name. Used in the API response.',
    )

    key_unique = models.Constraint('UNIQUE(key)', 'A category with this key already exists.')

    @api.depends('name')
    def _compute_key(self):
        for rec in self:
            rec.key = slugify(rec.name or '')

    def to_api_dict(self):
        return {
            'id': str(self.id),
            'name': self.name or '',
            'key': self.key or '',
        }
