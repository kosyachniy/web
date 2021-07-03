"""
Reports functionality for the API
"""

import json

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

    def _report(self, text, type_=0, extra=None, path=None, tags=[]):
        if self.mode != 'PROD' and type_ == 0:
            return

        preview = f"{SYMBOLS[type_]} {MODE} {TYPES[type_]}"

        if path:
            preview += "\n" + path

        text = preview + "\n\n" + text

        if extra:
            if isinstance(extra, dict):
                extra_text = "\n".join(f"{i} = {extra[i]}" for i in extra)
            else:
                extra_text = str(extra)

            text_with_extra = text + "\n\n" + extra_text
        else:
            text_with_extra = text

        tags = [self.mode.lower()] + tags
        text += "\n\n#" + " #".join(tags)
        text_with_extra += "\n\n#" + " #".join(tags)

        try:
            send_tg(BUG_CHAT, text_with_extra, markup=None)
        except Exception as error:
            if extra:
                print("❗️❗️❗️", error)
                print(extra)

                try:
                    send_tg(BUG_CHAT, text, markup=None)
                except Exception as error:
                    print("❗️❗️❗️", error)
                    print(type_, text)

            else:
                print("❗️❗️❗️", error)
                print(type_, text)


    def info(self, text, extra=None, path=None, tags=[]):
        self._report(text, 0, extra, path, tags)

    def warning(self, text, extra=None, path=None, tags=[]):
        self._report(text, 1, extra, path, tags)

    def error(self, text, extra=None, path=None, tags=[]):
        self._report(text, 2, extra, path, tags)

    def critical(self, text, extra=None, path=None, tags=[]):
        self._report(text, 3, extra, path, tags)

    def important(self, text, extra=None, path=None, tags=[]):
        self._report(text, 4, extra, path, tags)

    def request(self, text, extra=None, path=None, tags=[]):
        self._report(text, 5, extra, path, tags)


report = Report(MODE)
