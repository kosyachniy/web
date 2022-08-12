"""
Update sitemap.xml
"""

import time
import datetime
import asyncio

from api.lib import report


FILE_LIMIT = 2500
BODY = '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{}</sitemapindex>
'''
BODY_SUB = (
    '<?xml version="1.0" encoding="utf-8" standalone="no"?>'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{}</urlset>'
)
TEMPLATE = '''    <sitemap>
        <loc>https://cut-price.ru/{}</loc>
        <lastmod>{}</lastmod>
    </sitemap>
'''
TEMPLATE_SUB = (
    '<url>'
    '<loc>https://cut-price.ru/{}</loc>'
    '<lastmod>{}</lastmod>'
    '<changefreq>{}</changefreq>'
    '<priority>{}</priority>'
    '</url>'
)
LINKS = []
LINKS_SUB = [{
    'url': '',
    'time': time.time(),
    'freq': 'monthly',
    'priority': 0.9,
}]


def to_iso(data=datetime.datetime.utcnow()):
    """ Convert time to ISO for Sitemap """
    if isinstance(data, (int, float)):
        data = datetime.datetime.utcfromtimestamp(data)
    return data.replace(tzinfo=datetime.timezone.utc) \
               .replace(microsecond=0) \
               .isoformat()

async def generate_sitemap():
    """ Update sitemap.xml """

    links = LINKS + []

    data = ''
    for link in links:
        data += TEMPLATE.format(
            link['url'],
            time.strftime('%Y-%m-%d', time.gmtime(link['time'])),
            link['freq'],
            link['priority'],
        )

    with open('/data/sitemap.xml', 'w', encoding='utf-8') as file:
        print(BODY.format(data), file=file)


async def handle(_):
    """ Update sitemap.xml """

    while True:
        try:
            await generate_sitemap()
        # pylint: disable=broad-except
        except Exception as e:
            await report.critical(str(e), error=e)

        await asyncio.sleep(1800)  # 30 min
