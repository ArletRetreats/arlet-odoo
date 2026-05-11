{
    'name': 'Arlet CMS',
    'version': '18.0.1.0.0',
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
        'views/arlet_location_views.xml',
        'views/arlet_event_views.xml',
        'views/arlet_article_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
