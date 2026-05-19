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
        """Fetch all forms from HubSpot and upsert into this model (batch)."""
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

        # Paginate through all HubSpot forms
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
            after = (body.get('paging') or {}).get('next', {}).get('after')
            if not after:
                break

        # Build lookup of inbound data keyed by guid
        incoming = {}
        for form in all_forms:
            guid = form.get('id', '')
            if not guid:
                continue
            incoming[guid] = {
                'guid': guid,
                'portal_id': portal_id,
                'name': form.get('name', guid),
                'fields_json': [
                    {
                        'name': f.get('name', ''),
                        'label': f.get('label', ''),
                        'required': f.get('required', False),
                        'fieldType': f.get('fieldType', 'single_line_text'),
                    }
                    for group in form.get('fieldGroups', [])
                    for f in group.get('fields', [])
                    if not f.get('hidden')
                ],
            }

        # Single query to fetch all existing records
        existing_recs = self.search([('guid', 'in', list(incoming.keys()))])
        existing_by_guid = {r.guid: r for r in existing_recs}

        # Batch write existing, batch create new
        to_create = []
        for guid, vals in incoming.items():
            if guid in existing_by_guid:
                existing_by_guid[guid].write(vals)
            else:
                to_create.append(vals)
        if to_create:
            self.create(to_create)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'HubSpot Sync',
                'message': f'{len(incoming)} form(s) synced successfully.',
                'sticky': False,
                'type': 'success',
            },
        }
