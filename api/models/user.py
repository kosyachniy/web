"""
User model of DB object
"""

from consys.handlers import (
    default_login, check_login_uniq, check_password, process_password,
    check_name, check_surname, check_phone_uniq, pre_process_phone,
    check_mail_uniq, process_title, process_lower, default_status,
    default_title,
)

from models import Base, Attribute
from lib import cfg


class User(Base):
    """ User """

    _name = 'users'
    _search_fields = {
        'login',
        'name',
        'surname',
        'title',
        'phone',
        'mail',
        'description',
    }

    # status:
    # 0 - deleted
    # 1 - blocked
    # 2 - unauthorized
    # 3 - authorized
    # 4 - has access to platform resources
    # 5 - supervisor
    # 6 - moderator
    # 7 - admin
    # 8 - owner

    login = Attribute(
        types=str,
        default=default_login,
        checking=check_login_uniq,
        pre_processing=process_lower,
    )
    password = Attribute(
        types=str,
        checking=check_password,
        processing=process_password,
    )
    # Personal
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
    title = Attribute(
        types=str,
        default=default_title,
    )
    birth = Attribute(types=int) # TODO: datetime
    sex = Attribute(types=str) # TODO: enum: male / female
    # Contacts
    phone = Attribute(
        types=int,
        checking=check_phone_uniq,
        pre_processing=pre_process_phone,
    )
    phone_verified = Attribute(types=bool, default=True)
    mail = Attribute(
        types=str,
        checking=check_mail_uniq,
        pre_processing=process_lower,
    )
    mail_verified = Attribute(types=bool, default=True)
    social = Attribute(types=list) # TODO: list[{}] # TODO: checking
    #
    description = Attribute(types=str)
    status = Attribute(types=int, default=default_status)
    rating = Attribute(types=float)
    # global_channel = Attribute(types=int, default=1)
    # channels = Attribute(types=list)
    discount = Attribute(types=float)
    balance = Attribute(types=int, default=0)
    subscription = Attribute(types=int, default=0)
    utm = Attribute(types=str) # Source
    pay = Attribute(types=list) # Saved data for payment
    # Permissions
    mailing = Attribute(types=dict)
    # Cache
    last_online = Attribute(types=int)

    # TODO: UTM / promo
    # TODO: referal_parent
    # TODO: referal_code
    # TODO: attempts (password)
    # TODO: middle name

    # TODO: del Base.user

    def get_social(self, social):
        """ Get user social info by social ID """
        for i in self.social:
            if i['id'] == social:
                return {
                    'id': i['user'],
                    'login': i.get('login'),
                    'locale': i.get('locale') or cfg('locale'),
                }
        return None
