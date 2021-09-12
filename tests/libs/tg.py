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

    # Send message with markup
    await send(136563129, 'ola *bold* **text** ***bold*** _italic_ __text__ ___italic___ `code` ``text`` ```code```', markup='Markdown')
    await send(136563129, 'ola *bold* _italic_ __underline__ ~strikethrough~ `code`')
    await send(136563129, '*bold _italic bold ~italic bold strikethrough~ __underline italic bold___ bold*')
    await send(136563129, '[mention of a user](tg://user?id=136563129) [URL](http://www.example.com/)')
    await send(136563129, '```\npre-formatted fixed-width code block\n```')
    await send(136563129, '```python\npre-formatted fixed-width code block written in the Python programming language\n```')
    await send(136563129, 'ola *ola* _ola_`ola`', markup=None)
    await send(136563129, 'ola <b>bold</b> <strong>bold</strong> <i>italic</i> <em>italic</em> <u>underline</u> <ins>inderline</ins> <s>strikethrough</s> <strike>strikethrough</strike> <del>strikethrough</del> <code>inline fixed-width code</code>', markup='HTML')
    await send(136563129, '<b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>', markup='HTML')
    await send(136563129, '<a href="tg://user?id=136563129">mention of a user</a> <a href="http://www.example.com/">URL</a>', markup='HTML')
    await send(136563129, '<pre>pre-formatted fixed-width code block</pre>', markup='HTML')
    await send(136563129, '<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>', markup='HTML')

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
