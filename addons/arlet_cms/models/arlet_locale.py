from odoo import models, fields


class ArletLocale(models.Model):
    _name = 'arlet.locale'
    _description = 'Arlet Locale'
    _rec_name = 'name'
    _order = 'code asc'

    code = fields.Char(string='Code', required=True, help='ISO language code, e.g. "fr"')
    name = fields.Char(string='Language Name', required=True, help='e.g. "French"')

    _code_unique = models.Constraint('UNIQUE(code)', 'This locale code already exists.')
