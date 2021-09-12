import asyncio

from api.funcs.tg import send


async def main():
    # Send message
    await send(136563129, 'ola')
    await send([136563129, 136563129], 'ola')
    await send(136563129, 'ola', silent=True)
    await send(136563129, 'ola', reply=await send(136563129, 'ola'))
    await send(136563129, 'https://www.google.ru/')
    await send(136563129, 'https://www.google.ru/', preview=True)

    # Send media
    ## Buffer
    with open('test.png', 'rb') as file:
        await send(136563129, image=file)
    ## Bytes
    with open('test.png', 'rb') as file:
        image = file.read()
        await send(136563129, image=image)
    ## Path
    await send(136563129, image='test.png')
    ## Caption
    await send(136563129, 'ola', image='test.png')
    ## URL
    await send(136563129, 'ola', image='https://s1.1zoom.ru/big0/621/359909-svetik.jpg')
    ## Video
    await send(136563129, 'ola', video='test.mov')
    with open('test.mov', 'rb') as file:
        await send(136563129, video=file)
    await send(136563129, video='https://v16-web.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/5699531b06b74fbb80daf10e0f838873/?a=1988&br=1158&bt=579&cd=0%7C0%7C0&ch=0&cr=0&cs=0&dr=0&ds=3&er=&expire=1631466602&ft=9wMeRebG4kag3&l=20210912110948010190218226287C8320&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&policy=3&qs=0&rc=ajRqcmp3bHJxMzMzMzczM0ApNWk8aWQ3ZmRlNzgzNWk4NmdhLWQvcHJuNi1gLS01MTRzczI0MDQ1LzZfYDI1MWFgYGE6Yw%3D%3D&signature=d1d631ac890951da15d2d7ae33f9ba7a&tk=0&vl=&vr=')

    # Send message with markup
    ## Markdown
    await send(136563129, 'ola *bold* **text** ***bold*** _italic_ __text__ ___italic___ `code` ``text`` ```code```', markup='Markdown')
    ## Markdown 2
    await send(136563129, 'ola *bold* _italic_ __underline__ ~strikethrough~ `code`')
    await send(136563129, '*bold _italic bold ~italic bold strikethrough~ __underline italic bold___ bold*')
    await send(136563129, '[mention of a user](tg://user?id=136563129) [URL](http://www.example.com/)')
    await send(136563129, '```\npre-formatted fixed-width code block\n```')
    await send(136563129, '```python\npre-formatted fixed-width code block written in the Python programming language\n```')
    ## Without markup
    await send(136563129, 'ola *ola* _ola_`ola`', markup=None)
    ## HTML
    await send(136563129, 'ola <b>bold</b> <strong>bold</strong> <i>italic</i> <em>italic</em> <u>underline</u> <ins>inderline</ins> <s>strikethrough</s> <strike>strikethrough</strike> <del>strikethrough</del> <code>inline fixed-width code</code>', markup='HTML')
    await send(136563129, '<b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>', markup='HTML')
    await send(136563129, '<a href="tg://user?id=136563129">mention of a user</a> <a href="http://www.example.com/">URL</a>', markup='HTML')
    await send(136563129, '<pre>pre-formatted fixed-width code block</pre>', markup='HTML')
    await send(136563129, '<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>', markup='HTML')
    ## Invalid markup
    await send(136563129, 'ola <a>ola</b>', markup='HTML')
    ## Image & markup
    await send(136563129, '*bold*', ['x', 'y'], image='test.png')
    ## Recall path after wrong markup
    await send(136563129, '*bold_', ['x', 'y'], image='test.png')
    ## Recall buffer after wrong markup
    with open('test.png', 'rb') as file:
        await send(136563129, '*bold_', ['x', 'y'], image=file)

    # Send buttons
    await send(136563129, 'ola', ['x', 'y'])
    await send(136563129, 'ola', [['x', 'y'], 'zo'])
    await send(136563129, 'ola', [[{'name': 'Data', 'data': 'x'}], {'name': 'Link', 'data': 'https://www.google.ru/'}])
    await send(136563129, 'ola', None)
    await send(136563129, 'ola', [])

    # Edit buttons
    print(await send(136563129, 'ola', [[{'name': 'Data', 'data': 'x'}], {'name': 'Link', 'data': 'https://www.google.ru/'}]))


if __name__ == '__main__':
    asyncio.run(main())
