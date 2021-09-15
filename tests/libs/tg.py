import asyncio

from api.funcs.tg import send, edit, delete, check_entry, forward


async def main():
    # Send message
    print(await send(136563129, 'ola'))
    print(await send([136563129, 136563129], 'ola'))
    print(await send(136563129, 'ola', silent=True))
    print(await send(136563129, 'ola', reply=(await send(136563129, 'ola'))[0]))
    print(await send(136563129, 'https://www.google.ru/'))
    print(await send(136563129, 'https://www.google.ru/', preview=True))
    print(await send(136563129, 'x'*4097))

    # Send media
    ## Buffer
    with open('test.png', 'rb') as file:
        print(await send(136563129, files=file))
    ## Bytes
    with open('test.png', 'rb') as file:
        print(await send(136563129, files=file.read()))
    ## Path
    print(await send(136563129, files='test.png'))
    ## Caption
    print(await send(136563129, 'ola', files='test.png'))
    ## URL
    print(await send(136563129, 'ola', files='https://s1.1zoom.ru/big0/621/359909-svetik.jpg'))
    ## Video
    print(await send(136563129, 'ola', files={'data': 'test.mov', 'type': 'video'}))
    with open('test.mov', 'rb') as file:
        print(await send(136563129, files={'data': file, 'type': 'video'}))
    print(await send(136563129, files={'data': 'https://github.com/postbird/Mp4ToBlob/blob/master/video/v0-new.mp4?raw=true', 'type': 'video'}))
    ## Multi
    print(await send(136563129, 'ola', files=['test.png', 'test.png']))
    print(await send(136563129, 'ola', files=['test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png', 'test.png']))
    with open('test.png', 'rb') as file:
        print(await send(136563129, 'ola', files=['test.png', 'https://s1.1zoom.ru/big0/621/359909-svetik.jpg', file]))
    print(await send(136563129, 'ola', files=['test.png', {'data': 'test.mov', 'type': 'video'}]))
    with open('test.mov', 'rb') as file:
        print(await send(136563129, 'ola', files=['test.png', {'data': file, 'type': 'video'}]))
    with open('test.mov', 'rb') as file:
        print(await send(136563129, 'ola', files=['test.png', {'data': file.read(), 'type': 'video'}]))
    print(await send(136563129, 'ola', files=[{'data': 'test.mp3', 'type': 'audio'}, {'data': 'test.mp3', 'type': 'audio'}]))
    print(await send(136563129, 'ola', files=[{'data': 'test.txt', 'type': 'document'}, {'data': 'test.txt', 'type': 'document'}]))
    ## Audio
    print(await send(136563129, 'ola', files={'data': 'test.mp3', 'type': 'audio'}))
    print(await send(136563129, 'ola', files={'data': 'test.mp3', 'type': 'audio', 'title': 'Название', 'performer': 'Исполнитель'}))
    ## Animation
    print(await send(136563129, 'ola', files={'data': 'http://techslides.com/demos/sample-videos/small.mp4', 'type': 'animation'}))
    ## Voice
    print(await send(136563129, 'ola', files={'data': 'test.ogg', 'type': 'voice'}))
    ## Video note
    print(await send(136563129, files={'data': 'test.mp4', 'type': 'video_note', 'duration': 10, 'length': 100}))
    ## Location
    print(await send(136563129, files={'data': {'lat': 59.9392, 'lng': 30.3165}, 'type': 'location'}))
    ## Document
    print(await send(136563129, 'ola', files={'data': 'test.txt', 'type': 'document'}))
    ## Too long text
    print(await send(136563129, 'x'*1025, files='test.png'))

    # Send message with markup
    ## Markdown
    print(await send(136563129, 'ola *bold* **text** ***bold*** _italic_ __text__ ___italic___ `code` ``text`` ```code```', markup='Markdown'))
    ## Markdown 2
    print(await send(136563129, 'ola *bold* _italic_ __underline__ ~strikethrough~ `code`'))
    print(await send(136563129, '*bold _italic bold ~italic bold strikethrough~ __underline italic bold___ bold*'))
    print(await send(136563129, '[mention of a user](tg://user?id=136563129) [URL](http://www.example.com/)'))
    print(await send(136563129, '```\npre-formatted fixed-width code block\n```'))
    print(await send(136563129, '```python\npre-formatted fixed-width code block written in the Python programming language\n```'))
    ## Without markup
    print(await send(136563129, 'ola *ola* _ola_`ola`', markup=None))
    ## HTML
    print(await send(136563129, 'ola <b>bold</b> <strong>bold</strong> <i>italic</i> <em>italic</em> <u>underline</u> <ins>inderline</ins> <s>strikethrough</s> <strike>strikethrough</strike> <del>strikethrough</del> <code>inline fixed-width code</code>', markup='HTML'))
    print(await send(136563129, '<b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>', markup='HTML'))
    print(await send(136563129, '<a href="tg://user?id=136563129">mention of a user</a> <a href="http://www.example.com/">URL</a>', markup='HTML'))
    print(await send(136563129, '<pre>pre-formatted fixed-width code block</pre>', markup='HTML'))
    print(await send(136563129, '<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>', markup='HTML'))
    ## Invalid markup
    print(await send(136563129, 'ola <a>ola</b>', markup='HTML'))
    ## Image & markup
    print(await send(136563129, '*bold*', ['x', 'y'], files='test.png'))
    ## Recall path after wrong markup
    print(await send(136563129, '*bold_', ['x', 'y'], files='test.png'))
    ## Recall buffer after wrong markup
    with open('test.png', 'rb') as file:
        print(await send(136563129, '*bold_', ['x', 'y'], files=file))

    # Send buttons
    print(await send(136563129, 'ola', ['x', 'y']))
    print(await send(136563129, 'ola', [['x', 'y'], 'zo']))
    print(await send(136563129, 'ola', [[{'name': 'Data', 'data': 'x'}], {'name': 'Link', 'data': 'https://www.google.ru/'}]))
    print(await send(136563129, 'ola', None))
    print(await send(136563129, 'ola', []))

    # Edit
    print(await edit(
        136563129,
        (await send(136563129, 'ola', [[{'name': 'Data', 'data': 'x'}], {'name': 'Link', 'data': 'https://www.google.ru/'}]))[0],
        'ulu',
    ))
    print(await edit(
        136563129,
        (await send(136563129, 'ola', files='test.png'))[0],
        'ulu',
        files={'data': 'test.mov', 'type': 'video'},
    ))
    print(await edit(
        136563129,
        (await send(136563129, 'ola', files=['test.png', 'test.png']))[0],
        'ulu',
        files='test.jpg',
    ))
    print(await edit(
        136563129,
        (await send(136563129, 'ola'))[0],
        'ulu',
        [[{'name': 'Data', 'data': 'x'}], {'name': 'Link', 'data': 'https://www.google.ru/'}],
    ))

    # Delete
    print(await delete(
        136563129,
        (await send(136563129, 'ola'))[0],
    ))
    print(await delete(
        136563129,
        [((await send(136563129, 'ola'))[0], {123123123})],
    ))

    # Check entry
    print(await check_entry(-1001142824902, 136563129))
    print(await check_entry(0, 136563129))

    # Forward
    print(await forward(
        136563129,
        136563129,
        (await send(136563129, 'ola'))[0],
    ))


if __name__ == '__main__':
    asyncio.run(main())
