{
    'name': 'Arlet CMS',
    'version': '19.0.1.0.0',
    'category': 'Website/CMS',
    'summary': 'CMS data models and REST API for Arlet Next.js frontend',
    'description': (
        'Manages Events, Articles, and Locations. '
        'Exposes a public JSON REST API consumed by the Arlet Next.js frontend.'
    ),
    'author': 'Arlet',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/arlet_locale_data.xml',
        'data/arlet_page_config_data.xml',
        'views/arlet_locale_views.xml',
        'views/arlet_location_views.xml',
        'views/arlet_event_category_views.xml',
        'views/arlet_event_views.xml',
        'views/arlet_hubspot_views.xml',
        'views/arlet_article_views.xml',
        'views/arlet_page_config_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
