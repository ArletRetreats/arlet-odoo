import requests
from odoo import models, fields, api
from odoo.exceptions import UserError


class ArletHubspotForm(models.Model):
    _name = 'arlet.hubspot.form'
    _description = 'HubSpot Form (synced cache)'
    _rec_name = 'name'
    _order = 'name asc'

    portal_id = fields.Char(string='Portal ID', readonly=True)
    guid = fields.Char(string='Form GUID', required=True, readonly=True)
    name = fields.Char(string='Form Name', required=True, readonly=True)
    fields_json = fields.Json(string='Fields', readonly=True)

    _sql_constraints = [(
        'guid_unique', 'UNIQUE(guid)',
        'A form with this GUID already exists.',
    )]

    @api.model
    def _get_api_key(self):
        key = self.env['ir.config_parameter'].sudo().get_param('arlet.hubspot.api_key', '')
        if not key:
            raise UserError(
                'HubSpot API key is not configured. '
                'Go to Settings → Technical → System Parameters and set arlet.hubspot.api_key.'
            )
        return key

    @api.model
    def sync_from_hubspot(self):
        """Fetch all forms from HubSpot and upsert into this model."""
        api_key = self._get_api_key()
        headers = {'Authorization': f'Bearer {api_key}'}

        # Fetch portal ID from account info
        account_resp = requests.get(
            'https://api.hubapi.com/account-info/v3/details',
            headers=headers, timeout=15,
        )
        if not account_resp.ok:
            raise UserError(f'HubSpot account-info error {account_resp.status_code}: {account_resp.text}')
        portal_id = str(account_resp.json().get('portalId', '') or '')

        url = 'https://api.hubapi.com/marketing/v3/forms/'
        all_forms = []
        after = None

        while True:
            params = {'limit': 50}
            if after:
                params['after'] = after
            resp = requests.get(url, headers=headers, params=params, timeout=15)
            if not resp.ok:
                raise UserError(f'HubSpot API error {resp.status_code}: {resp.text}')
            body = resp.json()
            all_forms.extend(body.get('results', []))
            paging = body.get('paging', {})
            after = paging.get('next', {}).get('after')
            if not after:
                break

        for form in all_forms:
            guid = form.get('id', '')
            name = form.get('name', guid)
            fields_data = [
                {
                    'name': f.get('name', ''),
                    'label': f.get('label', ''),
                    'required': f.get('required', False),
                    'fieldType': f.get('fieldType', 'single_line_text'),
                }
                for group in form.get('fieldGroups', [])
                for f in group.get('fields', [])
                if not f.get('hidden')
            ]
            existing = self.search([('guid', '=', guid)], limit=1)
            if existing:
                existing.write({'name': name, 'portal_id': portal_id, 'fields_json': fields_data})
            else:
                self.create({'guid': guid, 'portal_id': portal_id, 'name': name, 'fields_json': fields_data})

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'HubSpot Sync',
                'message': f'{len(all_forms)} form(s) synced successfully.',
                'sticky': False,
                'type': 'success',
            },
        }
