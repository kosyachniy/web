"""
User model of DB object
"""

from consys.handlers import (
    default_login, check_login, check_password, process_password, check_name,
    check_surname, check_phone, pre_process_phone, check_mail, process_title,
    process_lower, default_status,
)

from . import Base, Attribute
from ..funcs import load_image, get_language


class User(Base):
    """ User """

    _name = 'users'
    _search_fields = {
        'login',
        'name',
        'surname',
        'phone',
        'mail',
        'description',
        # 'actions',
    }

    login = Attribute(
        types=str,
        default=default_login,
        checking=check_login,
        pre_processing=process_lower,
    )
    password = Attribute(
        types=str,
        checking=check_password,
        processing=process_password,
    )
    avatar = Attribute(types=str, processing=load_image)
    name = Attribute(
        types=str,
        checking=check_name,
        processing=process_title,
    )
    surname = Attribute(
        types=str,
        checking=check_surname,
        processing=process_title,
    )
    phone = Attribute(
        types=int,
        checking=check_phone,
        pre_processing=pre_process_phone,
    )
    phone_verified = Attribute(types=bool, default=True)
    mail = Attribute(
        types=str,
        checking=check_mail,
        pre_processing=process_lower,
    )
    mail_verified = Attribute(types=bool, default=True)
    social = Attribute(types=list, default=[]) # TODO: list[{}] # TODO: checking
    description = Attribute(types=str)
    language = Attribute(
        types=int,
        default=0,
        pre_processing=get_language,
    )
    status = Attribute(types=int, default=default_status)
    actions = Attribute(types=list, default=[]) # TODO: list[dict]
    online = Attribute(types=list, default=[]) # TODO: list[tuple]
    # TODO: UTM / promo
    # TODO: discount
    # TODO: balance
    # TODO: subscription
    # TODO: rating
    # TODO: referal_parent
    # TODO: referal_code
    # TODO: channels
    # TODO: attempts (password)
    # TODO: middle name

    # TODO: del Base.user
