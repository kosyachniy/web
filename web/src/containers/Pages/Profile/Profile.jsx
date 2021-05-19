import React, { useState } from 'react';
import { Redirect } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import api from '../../../func/api'
import Avatar from '../../../components/Avatar'


// const checkPassword = password => {
//     return (password.search(/\d/) !== -1) && (password.search(/[A-Za-z]/) !== -1);
// }

const Profile = (props) => {
    const { profile, profileUpdate } = props
    const { t } = useTranslation()
    const [login, setLogin] = useState(profile.login)
    const [name, setName] = useState(profile.name)
    const [surname, setSurname] = useState(profile.surname)
    const [mail, setMail] = useState(profile.mail)
    const [password, setPassword] = useState('')
    const [avatar, setAvatar] = useState(profile.avatar)
    const [file, setFile] = useState(null)

    const accountEdit = () => {
        const handlerSuccess = res => {
            profileUpdate({login, name, surname, mail, password, avatar})
        }

        const data = { login, name, surname, mail}

        if (password.length) {
            data['password'] = password
        }

        if (avatar !== profile.avatar) {
            data['avatar'] = avatar
            data['file'] = file
        }

        api('account.edit', data, handlerSuccess)
    }

    const updateAvatar = (avatar, file) => {
        setAvatar(avatar)
        setFile(file)
    }

    if (profile.id === 0) {
        return (
            <Redirect to="/" />
        )
    }

    return (
        <div className="album py-5">
            <div className="container">
                <Avatar avatar={avatar} file={file} updateAvatar={updateAvatar} />
                <form>
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
                        <div className="input-group-prepend">
                            <span className="input-group-text" id="addon-wrapping">@</span>
                        </div>
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
                    <div className="form-group">
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
                </form>
            </div>
        </div>
    );
};

export default Profile;