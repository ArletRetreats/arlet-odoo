from odoo import models, fields

# ---------------------------------------------------------------------------
# Page keys — one singleton record per page that needs configuration.
# New keys can be added here as more pages require CMS-driven content.
# ---------------------------------------------------------------------------
_PAGE_KEYS = [
    ('meet-arlet',        'Meet Arlet'),
    ('meet-marie',        'Meet Marie'),
    ('our-pillars',       'Our Pillars'),
    ('join-arlet',        'Join Arlet'),
    ('contact-us',        'Contact Us'),
    ('arlet-x-business',  'Arlet x Business'),
    ('arlet-x-you',       'Arlet x You'),
]


class ArletPageConfig(models.Model):
    _name = 'arlet.page.config'
    _description = 'Page Configuration'
    _rec_name = 'page_key'

    page_key = fields.Selection(
        _PAGE_KEYS,
        string='Page',
        required=True,
    )

    # ── HubSpot form (e.g. Contact Us page) ───────────────────────────
    hubspot_form_id = fields.Many2one(
        'arlet.hubspot.form',
        string='HubSpot Form',
        ondelete='set null',
        help='HubSpot form to embed on this page (e.g. Contact Us).',
    )

    # ── Featured article ────────────────────────────────────────────────
    featured_article_id = fields.Many2one(
        'arlet.article',
        string='Featured Article',
        domain=[('status', '=', 'published')],
        ondelete='set null',
        help='One article shown as an extra card on this page.',
    )

    # ── Testimonial profiles (e.g. Join Arlet page) ──────────────────────
    testimonial_profile_ids = fields.Many2many(
        'arlet.profile',
        'arlet_page_config_testimonial_rel',
        'config_id', 'profile_id',
        string='Testimonial Profiles',
        help='Profiles shown as testimonials on this page (displayed in order).',
    )

    # ── Featured events (e.g. Join Arlet → experience section) ─────────────
    featured_event_ids = fields.Many2many(
        'arlet.event',
        'arlet_page_config_event_rel',
        'config_id', 'event_id',
        string='Featured Events',
        help='Events shown as cards on this page (e.g. Join the Arlet Experience section).',
    )

    _sql_constraints = [(
        'page_key_unique', 'UNIQUE(page_key)',
        'A configuration record for this page already exists.',
    )]

    def to_api_dict(self, locale='en'):
        data = {'pageKey': self.page_key}
        if self.hubspot_form_id:
            data['hubspotForm'] = {
                'portalId': self.hubspot_form_id.portal_id or '',
                'guid': self.hubspot_form_id.guid or '',
                'fields': self.hubspot_form_id.fields_json or [],
            }
        if self.featured_article_id:
            data['featuredArticle'] = self.featured_article_id.to_list_api_dict(locale)
        if self.testimonial_profile_ids:
            data['testimonialProfiles'] = [p.to_api_dict(locale) for p in self.testimonial_profile_ids]
        if self.featured_event_ids:
            data['featuredEvents'] = [e._base_dict(locale) for e in self.featured_event_ids]
        return data
