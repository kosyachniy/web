"""
Reports functionality for the API
"""

import json
import inspect

from .tg_bot import send as send_tg


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())
    MODE = sets['mode']
    BUG_CHAT = sets['bug_chat']

SYMBOLS = ['🟢', '🟡', '🔴', '❗️', '✅', '🛎']
TYPES = ['INFO', 'WARNING', 'ERROR', 'CRITICAL', 'IMPORTANT', 'REQUEST']


class Report():
    """ Report logs and notifications on Telegram chat or in log files """

    def __init__(self, mode):
        self.mode = mode

    def _report(self, text, type_=0, extra=None, tags=None):
        if self.mode != 'PROD' and type_ == 0:
            return

        if not tags:
            tags = []

        previous = inspect.stack()[2]
        path = previous.filename.replace('/', '.').split('.')[2:-1]

        if path[0] == 'api':
            path = path[1:]

        if previous.function != 'handle':
            path.append(previous.function)

        path = '.'.join(path)

        text = f"{SYMBOLS[type_]} {MODE} {TYPES[type_]}" \
               f"\n{path}" \
               f"\n\n{text}"

        if extra:
            if isinstance(extra, dict):
                extra_text = "\n".join(f"{i} = {extra[i]}" for i in extra)
            else:
                extra_text = str(extra)

            text_with_extra = text + "\n\n" + extra_text
        else:
            text_with_extra = text

        tags = [self.mode.lower()] + tags
        outro = f"\n\n{previous.filename}:{previous.lineno}" \
                f"\n#" + " #".join(tags)

        text += outro
        text_with_extra += outro

        try:
            send_tg(BUG_CHAT, text_with_extra, markup=None)
        except Exception as e:
            if extra:
                print("❗️❗️❗️", e)
                print(extra)

                try:
                    send_tg(BUG_CHAT, text, markup=None)
                except Exception as e:
                    print("❗️❗️❗️", e)
                    print(type_, text)

            else:
                print("❗️❗️❗️", e)
                print(type_, text)


    def info(self, text, extra=None, tags=None):
        self._report(text, 0, extra, tags)

    def warning(self, text, extra=None, tags=None):
        self._report(text, 1, extra, tags)

    def error(self, text, extra=None, tags=None):
        self._report(text, 2, extra, tags)

    def critical(self, text, extra=None, tags=None):
        self._report(text, 3, extra, tags)

    def important(self, text, extra=None, tags=None):
        self._report(text, 4, extra, tags)

    def request(self, text, extra=None, tags=None):
        self._report(text, 5, extra, tags)


report = Report(MODE)
