"""
Update sitemap.xml
"""

import asyncio
import time

from api.lib import report


BODY = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{}</urlset>
'''
TEMPLATE = '''    <url>
        <loc>https://cut-price.ru/{}</loc>
        <lastmod>{}</lastmod>
        <changefreq>{}</changefreq>
        <priority>{}</priority>
    </url>
'''
LINKS = [{
    'url': '',
    'time': 1648684800,
    'freq': 'monthly',
    'priority': 0.9,
}]


async def generate_sitemap(_):
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

    with open('/data/sitemap.xml', 'w') as file:
        print(BODY.format(data), file=file)


async def handle(_):
    """ Update sitemap.xml """

    while True:
        try:
            await generate_sitemap(_)
        # pylint: disable=broad-except
        except Exception as e:
            await report.critical(str(e), error=e)

        await asyncio.sleep(1800)  # 30 min
