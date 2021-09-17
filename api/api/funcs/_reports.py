"""
Reports functionality for the API
"""

import json
import inspect
import traceback
import logging

from .tg import tg


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())
    MODE = sets['mode']
    BUG_CHAT = sets['bug_chat']

SYMBOLS = ['💬', '🟢', '🟡', '🔴', '❗️', '✅', '🛎']
TYPES = [
    'DEBUG', 'INFO',
    'WARNING', 'ERROR', 'CRITICAL',
    'IMPORTANT', 'REQUEST',
]


logger_err = logging.getLogger(__name__)
logger_log = logging.getLogger('info')


class Report():
    """ Report logs and notifications on Telegram chat or in log files """

    def __init__(self, mode):
        self.mode = mode

    async def _report(self, text, type_=0, extra=None, tags=None):
        """ Make report message and send """

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
            await tg.send(BUG_CHAT, text_with_extra, markup=None)

        except Exception:
            if extra:
                logger_err.error(
                    "%s  Send report  %s",
                    SYMBOLS[3], extra,
                )

                try:
                    await tg.send(BUG_CHAT, text, markup=None)
                except Exception:
                    logger_err.error(
                        "%s  Send report  %s %s",
                        SYMBOLS[3], type_, text,
                    )

            else:
                logger_err.error(
                    "%s  Send report  %s %s",
                    SYMBOLS[3], type_, text,
                )


    async def debug(self, text, extra=None):
        """ Debug
        Sequence of function calls, internal values
        """

        logger_log.debug("%s  %s  %s", SYMBOLS[0], text, json.dumps(extra))

    async def info(self, text, extra=None, tags=None):
        """ Info
        System logs and event journal
        """

        logger_log.info("%s  %s  %s", SYMBOLS[1], text, json.dumps(extra))
        await self._report(text, 1, extra, tags)

    async def warning(self, text, extra=None, tags=None):
        """ Warning
        Unexpected / strange code behavior that does not entail consequences
        """

        logger_err.warning("%s  %s  %s", SYMBOLS[2], text, json.dumps(extra))
        await self._report(text, 2, extra, tags)

    async def error(self, text, extra=None, tags=None, error=None):
        """ Error
        An unhandled error occurred
        """

        content = (
            "".join(
                traceback.format_exception(None, error, error.__traceback__)
            )
            if error is not None else
            f"{text}  {json.dumps(extra)}"
        )

        logger_err.error("%s  %s", SYMBOLS[3], content)
        await self._report(text, 3, extra, tags)

    async def critical(self, text, extra=None, tags=None, error=None):
        """ Critical
        An error occurred that affects the operation of the service
        """

        content = (
            "".join(
                traceback.format_exception(None, error, error.__traceback__)
            )
            if error is not None else
            f"{text}  {json.dumps(extra)}"
        )

        logger_err.critical("%s  %s", SYMBOLS[4], content)
        await self._report(text, 4, extra, tags)

    async def important(self, text, extra=None, tags=None):
        """ Important
        Trigger on tracked user action was fired
        """

        logger_log.info("%s  %s  %s", SYMBOLS[5], text, json.dumps(extra))
        await self._report(text, 5, extra, tags)

    async def request(self, text, extra=None, tags=None):
        """ Request
        The user made a request, the intervention of administrators is necessary
        """

        logger_log.info("%s  %s  %s", SYMBOLS[6], text, json.dumps(extra))
        await self._report(text, 6, extra, tags)


report = Report(MODE)
