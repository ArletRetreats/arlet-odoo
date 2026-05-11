from odoo import models, fields

# ---------------------------------------------------------------------------
# Page keys — one singleton record per page that needs configuration.
# New keys can be added here as more pages require CMS-driven content.
# ---------------------------------------------------------------------------
_PAGE_KEYS = [
    ('meet-arlet',   'Meet Arlet'),
    ('meet-marie',   'Meet Marie'),
    ('our-pillars',  'Our Pillars'),
    ('join-arlet',   'Join Arlet'),
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

    _sql_constraints = [(
        'page_key_unique', 'UNIQUE(page_key)',
        'A configuration record for this page already exists.',
    )]

    def to_api_dict(self, locale='en'):
        data = {'pageKey': self.page_key}
        if self.featured_article_id:
            data['featuredArticle'] = self.featured_article_id.to_list_api_dict(locale)
        if self.testimonial_profile_ids:
            data['testimonialProfiles'] = [p.to_api_dict(locale) for p in self.testimonial_profile_ids]
        return data
