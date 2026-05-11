import os

from odoo import http
from odoo.http import request

# ---------------------------------------------------------------------------
# Configuration — set these environment variables before starting Odoo.
#
#   ARLET_CORS_ORIGIN   Allowed CORS origin, e.g. "https://arlet.com"
#                       Defaults to "*" (open) when not set.
#
#   ARLET_API_KEY       Shared secret. When set, every request must include:
#                           X-Api-Key: <value>
#                       Leave unset (or empty) to disable key enforcement.
# ---------------------------------------------------------------------------
_CORS = os.environ.get('ARLET_CORS_ORIGIN', '*')
_API_KEY = os.environ.get('ARLET_API_KEY', '')
_VALID_LOCALES = ('en', 'fr')


class ArletApiController(http.Controller):

    def _check_api_key(self):
        """Return a 401 JSON response if the API key is wrong, else None."""
        if not _API_KEY:
            return None
        provided = request.httprequest.headers.get('X-Api-Key', '')
        if provided != _API_KEY:
            return request.make_json_response({'error': 'Unauthorized'}, status=401)
        return None

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
        err = self._check_api_key()
        if err:
            return err
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
        err = self._check_api_key()
        if err:
            return err
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
        err = self._check_api_key()
        if err:
            return err
        locale = locale if locale in _VALID_LOCALES else 'en'
        article = request.env['arlet.article'].sudo().search(
            [('slug', '=', slug), ('status', '=', 'published')],
            limit=1,
        )
        if not article:
            return request.make_json_response(None, status=404)
        return request.make_json_response(article.to_detail_api_dict(locale))

    # ------------------------------------------------------------------
    # GET /api/arlet/locales
    # ------------------------------------------------------------------
    @http.route(
        '/api/arlet/locales',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False,
        cors=_CORS,
    )
    def list_locales(self, **kwargs):
        err = self._check_api_key()
        if err:
            return err
        locales = request.env['arlet.locale'].sudo().search([], order='code asc')
        # Always prepend EN (the base language — not stored in arlet.locale)
        data = [{'code': 'en', 'name': 'English'}] + [
            {'code': loc.code, 'name': loc.name} for loc in locales
        ]
        return request.make_json_response(data)

    # ------------------------------------------------------------------
    # GET /api/arlet/locations
    # ------------------------------------------------------------------
    # GET /api/arlet/events/<slug>?locale=en
    # ------------------------------------------------------------------
    @http.route(
        '/api/arlet/events/<string:slug>',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False,
        cors=_CORS,
    )
    def get_event_by_slug(self, slug, locale='en', **kwargs):
        err = self._check_api_key()
        if err:
            return err
        locale = locale if locale in _VALID_LOCALES else 'en'
        event = request.env['arlet.event'].sudo().search(
            [('slug', '=', slug)],
            limit=1,
        )
        if not event:
            return request.make_json_response(None, status=404)
        return request.make_json_response(event.to_detail_api_dict(locale))

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
        err = self._check_api_key()
        if err:
            return err
        locations = request.env['arlet.location'].sudo().search([])
        data = [loc.to_list_api_dict() for loc in locations]
        return request.make_json_response(data)
