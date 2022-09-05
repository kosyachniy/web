import { useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { useTranslation } from 'next-i18next'

import { popupSet, profileIn } from '../store'
import api from '../functions/api'
import styles from '../styles/mail.module.css'
import Popup from './Popup'


const checkPassword = password => {
    return (password.search(/\d/) !== -1) && (password.search(/[A-Za-z]/) !== -1)
}

export default () => {
    const { t } = useTranslation('common')
    const dispatch = useDispatch()
    const system = useSelector((state) => state.system)
    const [mail, setMail] = useState('')
    const [password, setPassword] = useState('')

    const signIn = (event) => {
        api(
            system.token, system.locale,
            'account.auth',
            {login: mail, password}
        ).then(res => {
            dispatch(profileIn(res))
            dispatch(popupSet(null))
        })

        event.preventDefault();
    }

    return (
        <div>
            <Popup>
                <form onSubmit={signIn}>
                    <div className="input-group mb-3">
                        <input
                            className="form-control"
                            type="text"
                            placeholder={t('profile.mail')}
                            value={mail}
                            onChange={ (event) => { setMail(event.target.value) } }
                            autoComplete="off"
                            required
                        />
                    </div>
                    <div className="input-group mb-3">
                        <input
                            className="form-control"
                            // className={ (responce !== null && responce.data === 'password') ? 'error' : '' }
                            type="password"
                            placeholder={ t('profile.password') }
                            value={ password }
                            onChange={ (event) => { setPassword(event.target.value) } }
                            autoComplete="off"
                            required
                        />
                    </div>
                    <div className={ styles.pass_info }>
                        <span style={ password.length >= 6 ? {} : { color: '#e74c3c' } }>
                            <i className="fas fa-genderless" />
                            { t('profile.passwordTip1') }
                        </span>
                        <span style={ checkPassword(password) ? {} : { color: '#e74c3c' } }>
                            <i className="fas fa-genderless" />
                            { t('profile.passwordTip2') }
                        </span>
                    </div>
                    {/* <input
                        type="submit"
                        className="btn btn-success"
                        value={t('system.sign_in')}
                    /> */}
                </form>
            </Popup>
        </div>
    )
}
