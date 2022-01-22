import React, { useState, useEffect } from 'react';
import { Redirect } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import api from '../../../lib/api'
import Avatar from '../../../components/Avatar'


// const checkPassword = password => {
//     return (password.search(/\d/) !== -1) && (password.search(/[A-Za-z]/) !== -1);
// }

const Profile = (props) => {
    const { profile, profileUpdate } = props
    const { t } = useTranslation()
    const [login, setLogin] = useState(profile.login || '')
    const [password, setPassword] = useState('')
    const [avatar, setAvatar] = useState(profile.avatar)
    const [name, setName] = useState(profile.name || '')
    const [surname, setSurname] = useState(profile.surname || '')
    const [phone, setPhone] = useState(profile.phone || '')
    const [mail, setMail] = useState(profile.mail || '')
    // const [social, setSocial] = useState(profile.social)
    // const [status, setStatus] = useState(profile.status)

    useEffect(() => {
        api('users.get', {id: +profile.id}).then(res => {
            profileUpdate({
                login: res.users.login,
                avatar: res.users.avatar,
                name: res.users.name,
                surname: res.users.surname,
                phone: res.users.phone,
                mail: res.users.mail,
                social: res.users.social,
                status: res.users.status,
            })
        })
    }, [])

    if (profile.id === 0) {
        return (
            <Redirect to="/" />
        )
    }

    const accountEdit = () => {
        const data = {}

        if (login && login !== profile.login) {
            data['login'] = login
        }

        if (name && name !== profile.name) {
            data['name'] = name
        }

        if (surname && surname !== profile.surname) {
            data['surname'] = surname
        }

        if (phone && phone !== profile.phone) {
            data['phone'] = phone
        }

        if (mail && mail !== profile.mail) {
            data['mail'] = mail
        }

        if (password.length) {
            data['password'] = password
        }

        if (avatar !== profile.avatar) {
            data['avatar'] = avatar
        }

        api('account.save', data).then(res => {
            profileUpdate({login, avatar, name, surname, phone, mail})
        })
    }

    return (
        <div className="container">
            <Avatar avatar={avatar} setAvatar={setAvatar} />
            <div className="input-group mb-3">
                <input
                    value={name}
                    onChange={(event) => { setName(event.target.value) }}
                    placeholder={t('profile.name')}
                    type="text"
                    aria-label="First name"
                    className="form-control"
                />
                <input
                    value={surname}
                    onChange={(event) => { setSurname(event.target.value) }}
                    placeholder={t('profile.surname')}
                    type="text"
                    aria-label="Last name"
                    className="form-control"
                />
            </div>
            <div className="input-group flex-nowrap mb-3">
                <span className="input-group-text" id="addon-wrapping">+</span>
                <input
                    value={phone}
                    onChange={(event) => { setPhone(event.target.value) }}
                    placeholder={t('profile.phone')}
                    type="text"
                    className="form-control"
                    aria-label="Phone number"
                    aria-describedby="addon-wrapping"
                />
            </div>
            <div className="input-group flex-nowrap mb-3">
                <span className="input-group-text" id="addon-wrapping">@</span>
                <input
                    value={login}
                    onChange={(event) => { setLogin(event.target.value) }}
                    placeholder={t('profile.login')}
                    type="text"
                    className="form-control"
                    aria-label="Username"
                    aria-describedby="addon-wrapping"
                />
            </div>
            <div className="input-group mb-3">
                <input
                    value={mail}
                    onChange={(event) => { setMail(event.target.value) }}
                    placeholder={t('profile.mail')}
                    type="email"
                    className="form-control"
                    autoComplete="false"
                />
            </div>
            <div className="input-group mb-3">
                <input
                    value={password}
                    onChange={(event) => { setPassword(event.target.value) }}
                    placeholder={t('profile.password')}
                    type="password"
                    className="form-control"
                    autoComplete="false"
                />
            </div>
            <input
                type="button"
                className="btn btn-success"
                value={t('system.save')}
                onClick={accountEdit}
            />
        </div>
    );
};

export default Profile;
