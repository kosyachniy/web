# -*- coding: utf-8 -*-
# NOTE: SMSC.RU API (smsc.ru) версия 1.9 (01.02.2017)

"""
Sending SMS messages
"""

# pylint: disable=all

import json
from datetime import datetime
import smtplib

try:
    from urllib import urlopen, quote
except ImportError:
    from urllib.request import urlopen
    from urllib.parse import quote

from . import report


with open('sets.json', 'r') as file:
    s = json.loads(file.read())['smsc']

# Константы для настройки библиотеки
SMSC_LOGIN = s['login'] # логин клиента
SMSC_PASSWORD = s['password'] # пароль или MD5-хеш пароля в нижнем регистре
SMSC_POST = False # использовать метод POST
SMSC_HTTPS = False # использовать HTTPS протокол
SMSC_CHARSET = "utf-8" # кодировка (windows-1251 / koi8-r / utf-8)
SMSC_DEBUG = False # флаг отладки

# Константы для отправки SMS по SMTP
SMTP_FROM = "api@smsc.ru" # e-mail адрес отправителя
SMTP_SERVER = "send.smsc.ru" # адрес smtp сервера
SMTP_LOGIN = "" # логин для smtp сервера
SMTP_PASSWORD = "" # пароль для smtp сервера


def ifs(cond, val1, val2):
    """ Вспомогательная функция, эмуляция тернарной операции ?: """
    if cond:
        return val1
    return val2


class SMSC():
    """ Класс для взаимодействия с сервером smsc.ru """

    def send_sms(
        self, phones, message, translit=0, time="",
        id_=0, format=0, sender=False, query="",
    ):
        """ Метод отправки SMS """
        """
        обязательные параметры:

        phones - список телефонов через запятую или точку с запятой
        message - отправляемое сообщение

        необязательные параметры:

        translit - переводить или нет в транслит (1,2 или 0)
        time - необходимое время доставки в виде строки
        (DDMMYYhhmm, h1-h2, 0ts, +m)
        id - идентификатор сообщения.
        Представляет собой 32-битное число в диапазоне от 1 до 2147483647.
        format - формат сообщения (0 - обычное sms, 1 - flash-sms, 2 - wap-push,
        3 - hlr, 4 - bin, 5 - bin-hex, 6 - ping-sms, 7 - mms, 8 - mail, 9 - call)
        sender - имя отправителя (Sender ID). Для отключения Sender ID по
        умолчанию необходимо в качестве имени передать пустую строку или точку.
        query - строка дополнительных параметров, добавляемая в URL-запрос
        ("valid=01:00&maxsms=3")

        возвращает массив (<id>, <количество sms>, <стоимость>, <баланс>) в случае
        успешной отправки либо массив (<id>, -<код ошибки>) в случае ошибки
        """

        formats = [
            "flash=1", "push=1", "hlr=1", "bin=1", "bin=2",
            "ping=1", "mms=1", "mail=1", "call=1",
        ]

        res = self._smsc_send_cmd("send", "cost=3&phones=" + quote(phones) \
            + "&mes=" + quote(message) + "&translit=" + str(translit) + "&id=" \
            + str(id_) + ifs(format > 0, "&" + formats[format-1], "") \
            + ifs(sender is False, "", "&sender=" + quote(str(sender)))
            + ifs(time, "&time=" + quote(time), "") \
            + ifs(query, "&" + query, ""))

        # (id, cnt, cost, balance) или (id, -error)

        if SMSC_DEBUG:
            if res[1] > "0":
                report.debug(
                    "Сообщение отправлено успешно. ID: " + res[0] \
                    + ", всего SMS: " + res[1] + ", стоимость: " + res[2] \
                    + ", баланс: " + res[3]
                )
            else:
                report.error(
                    "Ошибка №" + res[1][1:] \
                    + ifs(res[0] > "0", ", ID: " + res[0], "")
                )

        return res

    def send_sms_mail(
        self, phones, message, translit=0, time="", id_=0, format=0, sender="",
    ):
        """ SMTP версия метода отправки SMS """

        server = smtplib.SMTP(SMTP_SERVER)

        if SMSC_DEBUG:
            server.set_debuglevel(1)

        if SMTP_LOGIN:
            server.login(SMTP_LOGIN, SMTP_PASSWORD)

        server.sendmail(
            SMTP_FROM, "send@send.smsc.ru", \
            "Content-Type: text/plain; charset=" + SMSC_CHARSET + "\n\n" \
            + SMSC_LOGIN + ":" + SMSC_PASSWORD + ":" + str(id_) + ":" + time \
            + ":" + str(translit) + "," + str(format) + "," + sender + ":" \
            + phones + ":" + message,
        )
        server.quit()

    def get_sms_cost(
        self, phones, message, translit=0, format=0, sender=False, query="",
    ):
        """ Метод получения стоимости SMS """
        """
        обязательные параметры:

        phones - список телефонов через запятую или точку с запятой
        message - отправляемое сообщение

        необязательные параметры:

        translit - переводить или нет в транслит (1,2 или 0)
        format - формат сообщения (0 - обычное sms, 1 - flash-sms, 2 - wap-push,
        3 - hlr, 4 - bin, 5 - bin-hex, 6 - ping-sms, 7 - mms, 8 - mail, 9 - call)
        sender - имя отправителя (Sender ID)
        query - строка дополнительных параметров, добавляемая в URL-запрос
        ("list=79999999999:Ваш пароль: 123\n78888888888:Ваш пароль: 456")

        возвращает массив (<стоимость>, <количество sms>) либо массив
        (0, -<код ошибки>) в случае ошибки
        """

        formats = [
            "flash=1", "push=1", "hlr=1", "bin=1", "bin=2",
            "ping=1", "mms=1", "mail=1", "call=1",
        ]

        res = self._smsc_send_cmd(
            "send", "cost=1&phones=" + quote(phones) + "&mes=" \
            + quote(message) + ifs(sender is False, "", "&sender=" \
            + quote(str(sender))) + "&translit=" + str(translit) \
            + ifs(format > 0, "&" + formats[format-1], "") \
            + ifs(query, "&" + query, ""),
        )

        # (cost, cnt) или (0, -error)

        if SMSC_DEBUG:
            if res[1] > "0":
                report.debug(
                    "Стоимость рассылки: " + res[0] + ". Всего SMS: " + res[1]
                )
            else:
                report.error("Ошибка №" + res[1][1:])

        return res

    def get_status(self, id_, phone, all = 0):
        """ Метод проверки статуса отправленного SMS или HLR-запроса """
        """
        id_ - ID cообщения
        phone - номер телефона

        возвращает массив:
        для отправленного SMS (<статус>, <время изменения>, <код ошибки sms>)
        для HLR-запроса (<статус>, <время изменения>, <код ошибки sms>,
        <код IMSI SIM-карты>, <номер сервис-центра>, <код страны регистрации>,
        <код оператора абонента>, <название страны регистрации>,
        <название оператора абонента>, <название роуминговой страны>,
        <название роумингового оператора>)

        При all = 1 дополнительно возвращаются элементы в конце массива:
        (<время отправки>, <номер телефона>, <стоимость>, <sender id>,
        <название статуса>, <текст сообщения>)

        либо массив (0, -<код ошибки>) в случае ошибки
        """

        res = self._smsc_send_cmd(
            "status",
            "phone=" + quote(phone) + "&id=" + str(id_) + "&all=" + str(all),
        )

        # (status, time, err, ...) или (0, -error)

        if SMSC_DEBUG:
            if res[1] >= "0":
                text = ""
                if res[1] > "0":
                    text = str(datetime.fromtimestamp(int(res[1])))
                report.debug(
                    "Статус SMS = " + res[0] + ifs(
                        res[1] > "0",
                        ", время изменения статуса - " + text,
                        "",
                    ),
                )
            else:
                report.error("Ошибка №" + res[1][1:])

        if all and len(res) > 9 and (len(res) < 14 or res[14] != "HLR"):
            res = (",".join(res)).split(",", 8)

        return res

    def get_balance(self):
        """ Метод получения баланса """
        """
        без параметров

        возвращает баланс в виде строки или False в случае ошибки
        """

        res = self._smsc_send_cmd("balance") # (balance) или (0, -error)

        if SMSC_DEBUG:
            if len(res) < 2:
                report.debug("Сумма на счете: " + res[0])
            else:
                report.error("Ошибка №" + res[1][1:])

        return ifs(len(res) > 1, False, res[0])


    # ВНУТРЕННИЕ МЕТОДЫ

    def _smsc_send_cmd(self, cmd, arg=""):
        """ Метод вызова запроса """
        """
        Формирует URL и делает 3 попытки чтения
        """

        url = ifs(SMSC_HTTPS, "https", "http") + "://smsc.ru/sys/" + cmd \
            + ".php"
        _url = url
        arg = "login=" + quote(SMSC_LOGIN) + "&psw=" + quote(SMSC_PASSWORD) \
            + "&fmt=1&charset=" + SMSC_CHARSET + "&" + arg

        i = 0
        ret = ""

        while ret == "" and i <= 5:
            if i > 0:
                url = _url.replace("smsc.ru/", "www" + str(i) + ".smsc.ru/")
            else:
                i += 1

            try:
                if SMSC_POST or len(arg) > 2000:
                    data = urlopen(url, arg.encode(SMSC_CHARSET))
                else:
                    data = urlopen(url + "?" + arg)

                ret = str(data.read().decode(SMSC_CHARSET))
            except:
                ret = ""

            i += 1

        if ret == "":
            if SMSC_DEBUG:
                report.error("Ошибка чтения адреса: " + url)
            ret = "," # фиктивный ответ

        return ret.split(",")


# Examples:
# smsc = SMSC()
# smsc.send_sms("79999999999", "test", sender="sms")
# smsc.send_sms("79999999999", "http://smsc.ru\nSMSC.RU", query="maxsms=3")
# smsc.send_sms("79999999999", "0605040B8423F0DC0601AE02056A0045C60C036D7973697\
# 4652E72750001036D7973697465000101", format=5)
# smsc.send_sms("79999999999", "", format=3)
# r = smsc.get_sms_cost("79999999999", "Вы успешно зарегистрированы!")
# smsc.send_sms_mail("79999999999", "test2", format=1)
# r = smsc.get_status(12345, "79999999999")
# report.important(smsc.get_balance())
