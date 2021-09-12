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
        await send(136563129, files=file)
    ## Bytes
    with open('test.png', 'rb') as file:
        await send(136563129, files=file.read())
    ## Path
    await send(136563129, files='test.png')
    ## Caption
    await send(136563129, 'ola', files='test.png')
    ## URL
    await send(136563129, 'ola', files='https://s1.1zoom.ru/big0/621/359909-svetik.jpg')
    ## Video
    await send(136563129, 'ola', files={'data': 'test.mov', 'type': 'video'})
    with open('test.mov', 'rb') as file:
        await send(136563129, files={'data': file, 'type': 'video'})
    await send(136563129, files={'data': 'https://github.com/postbird/Mp4ToBlob/blob/master/video/v0-new.mp4?raw=true', 'type': 'video'})
    ## Multi
    await send(136563129, 'ola', files=['test.png', 'test.png'])
    with open('test.png', 'rb') as file:
        await send(136563129, 'ola', files=['test.png', 'https://s1.1zoom.ru/big0/621/359909-svetik.jpg', file])
    await send(136563129, 'ola', files=['test.png', {'data': 'test.mov', 'type': 'video'}])
    ## Audio
    await send(136563129, 'ola', files={'data': 'test.mp3', 'type': 'audio'})
    await send(136563129, 'ola', files={'data': 'test.mp3', 'type': 'audio', 'title': 'Название', 'performer': 'Исполнитель'})
    ## Animation
    await send(136563129, 'ola', files={'data': 'http://techslides.com/demos/sample-videos/small.mp4', 'type': 'animation'})
    ## Voice
    await send(136563129, 'ola', files={'data': 'test.ogg', 'type': 'voice'})
    ## Video note
    await send(136563129, files={'data': 'test.mp4', 'type': 'video_note', 'duration': 10, 'length': 100})
    ## Location
    await send(136563129, files={'data': {'lat': 59.9392, 'lng': 30.3165}, 'type': 'location'})
    ## Document
    await send(136563129, 'ola', files={'data': 'test.txt', 'type': 'document'})

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
    await send(136563129, '*bold*', ['x', 'y'], files='test.png')
    ## Recall path after wrong markup
    await send(136563129, '*bold_', ['x', 'y'], files='test.png')
    ## Recall buffer after wrong markup
    with open('test.png', 'rb') as file:
        await send(136563129, '*bold_', ['x', 'y'], files=file)

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
