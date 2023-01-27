"""
Update sitemaps
"""

import time
import datetime
import gzip
import shutil
import asyncio

from lib import cfg, report
from models.category import Category
from models.post import Post


LOCALES = ['en', 'ru']
FILE_LINKS_LIMIT = None # 2500
FILES_LIMIT = None # 1000
BODY = '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{}</sitemapindex>
'''
BODY_SUB = (
    '<?xml version="1.0" encoding="utf-8" standalone="no"?>'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{}</urlset>'
)
TEMPLATE = '''    <sitemap>
        <loc>{}{}</loc>
        <lastmod>{}</lastmod>
    </sitemap>
'''
LINKS_SUB = [{
    'url': '',
    'time': time.time(),
    'freq': 'weekly',
    'priority': 0.9,
}]
ROBOTS = f'''
User-agent: *

Disallow: /api
Disallow: /eye
Disallow: /grafana
Disallow: /prometheus
Disallow: /callback
Disallow: /profile

Sitemap: {cfg('web')}sitemap.xml
'''
ROBOTS_OFF = '''
User-agent: *
Disallow: /
'''


def to_iso(data=datetime.datetime.utcnow()):
    """ Convert time to ISO for Sitemap """
    if isinstance(data, (int, float)):
        data = datetime.datetime.utcfromtimestamp(data)
    return data.replace(tzinfo=datetime.timezone.utc) \
               .replace(microsecond=0) \
               .isoformat()

async def generate_file(links, locale=None, kind=None, ind=None):
    """ Generate a file of sub sitemap """

    data = ""
    for link in links:
        sublink = (
            cfg('web')
            + ('' if not locale or locale == cfg('locale') else locale + '/')
            + link['url']
        )
        data += (
            f"<url><loc>{sublink}</loc>"
            f"<lastmod>{to_iso(link['time'])}</lastmod>"
        )
        if link.get('freq'):
            data += f"<changefreq>{link['freq']}</changefreq>"
        if link.get('priority'):
            data += f"<priority>{link['priority']}</priority>"
        data += "</url>"

    blocks = [locale, 'sitemap', kind, ind]
    sitemap_name = (
        'sitemaps/'
        + '-'.join([str(block) for block in blocks if block])
        + '.xml'
    )
    with open(f'/data/{sitemap_name}', 'w', encoding='utf-8') as file:
        print(BODY_SUB.format(data), file=file)

    with open(f'/data/{sitemap_name}', 'rb') as f_in:
        sitemap_name += '.gz'
        with gzip.open(f'/data/{sitemap_name}', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    return sitemap_name

async def generate_sitemap():
    """ Update sitemap.xml """

    timestamp = datetime.datetime.utcnow()
    links = []

    # Main pages
    links_sub = []
    for locale in LOCALES:
        links_sub.append({
            'url': '' if locale == cfg('locale') else locale + '/',
            'time': timestamp,
            'freq': 'daily',
            'priority': 0.9,
        })

    url = await generate_file(links_sub)
    links.append({
        'url': url,
        'time': timestamp,
    })

    # Categories
    for locale in [None] + LOCALES:
        links_sub = []
        for category in Category.get(
            locale=locale if locale else {'$nin': LOCALES},
        ):
            links_sub.append({
                'url': f'posts/{category.url}/',
                'time': timestamp,
                'freq': 'daily',
                'priority': 0.8,
            })

        url = await generate_file(links_sub, locale, 'categories')
        links.append({
            'url': url,
            'time': timestamp,
        })

    # Posts
    for locale in [None] + LOCALES:
        links_sub = []
        last_update = 0
        for post in Post.get(
            locale=locale if locale else {'$nin': LOCALES},
        ):
            last_update = max(last_update, post.updated)
            links_sub.append({
                'url': f'posts/{post.id}/',
                'time': post.updated,
                'freq': 'daily',
                'priority': 0.7,
            })

        url = await generate_file(links_sub, locale, 'posts', 1)
        links.append({
            'url': url,
            'time': last_update,
        })

    # Generate main sitemap
    data = ''
    for link in links:
        data += TEMPLATE.format(
            cfg('web'),
            link['url'],
            to_iso(link.get('time')),
        )
    with open('/data/sitemap.xml', 'w', encoding='utf-8') as file:
        print(BODY.format(data), file=file)


async def handle(_):
    """ Update sitemap.xml """

    with open('/data/robots.txt', 'w', encoding='utf-8') as file:
        if cfg('mode') == 'PROD':
            print(ROBOTS, file=file)
        else:
            print(ROBOTS_OFF, file=file)

    while True:
        try:
            await generate_sitemap()
        # pylint: disable=broad-except
        except Exception as e:
            await report.critical(str(e), error=e)

        await asyncio.sleep(3600)  # 1 hour
