from odoo import http
from odoo.http import request

# Restrict CORS to your frontend origin in production, e.g.:
# CORS_ORIGIN = 'https://arlet.com'
# For local dev, '*' is used.
_CORS = '*'
_VALID_LOCALES = ('en', 'fr')


class ArletApiController(http.Controller):

    # ------------------------------------------------------------------
    # GET /api/arlet/events?locale=en
    # ------------------------------------------------------------------
    @http.route(
        '/api/arlet/events',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False,
        cors=_CORS,
    )
    def list_events(self, locale='en', **kwargs):
        locale = locale if locale in _VALID_LOCALES else 'en'
        events = request.env['arlet.event'].sudo().search([])
        data = [event.to_api_dict(locale) for event in events]
        return request.make_json_response(data)

    # ------------------------------------------------------------------
    # GET /api/arlet/articles?locale=en
    # ------------------------------------------------------------------
    @http.route(
        '/api/arlet/articles',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False,
        cors=_CORS,
    )
    def list_articles(self, locale='en', **kwargs):
        locale = locale if locale in _VALID_LOCALES else 'en'
        articles = request.env['arlet.article'].sudo().search([])
        data = [article.to_list_api_dict(locale) for article in articles]
        return request.make_json_response(data)

    # ------------------------------------------------------------------
    # GET /api/arlet/articles/<slug>?locale=en
    # ------------------------------------------------------------------
    @http.route(
        '/api/arlet/articles/<string:slug>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False,
        cors=_CORS,
    )
    def get_article_by_slug(self, slug, locale='en', **kwargs):
        locale = locale if locale in _VALID_LOCALES else 'en'
        article = request.env['arlet.article'].sudo().search(
            [('slug', '=', slug), ('status', '=', 'published')],
            limit=1,
        )
        if not article:
            return request.make_json_response(None, status=404)
        return request.make_json_response(article.to_detail_api_dict(locale))

    # ------------------------------------------------------------------
    # GET /api/arlet/locations
    # ------------------------------------------------------------------
    @http.route(
        '/api/arlet/locations',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False,
        cors=_CORS,
    )
    def list_locations(self, **kwargs):
        locations = request.env['arlet.location'].sudo().search([])
        data = [loc.to_list_api_dict() for loc in locations]
        return request.make_json_response(data)
