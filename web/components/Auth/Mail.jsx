import { useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { useTranslation } from 'next-i18next'
import Button from 'react-bootstrap/Button'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import { popupSet } from '../../redux/actions/system'
import { profileIn } from '../../redux/actions/profile'
import api from '../../lib/api'
import styles from '../../styles/mail.module.css'
import Popup from '../Popup'


const checkPassword = password => (
    (password.search(/\d/) !== -1) && (password.search(/[A-Za-z]/) !== -1)
)

export default () => {
    const { t } = useTranslation('common')
    const dispatch = useDispatch()
    const main = useSelector(state => state.main)
    const [mail, setMail] = useState('')
    const [password, setPassword] = useState('')

    const signIn = event => {
        api(main, 'account.auth', {
            login: mail,
            password,
            utm: main.utm,
        }).then(res => {
            dispatch(profileIn(res))
            dispatch(popupSet(null))
        })

        event.preventDefault()
    }

    return (
        <div>
            <Popup>
                <form onSubmit={signIn}>
                    <div className="input-group mb-3">
                        <input
                            className="form-control"
                            type="text"
                            placeholder={ t('profile.mail') }
                            value={mail}
                            onChange={ event => setMail(event.target.value) }
                            autoComplete="off"
                            required
                        />
                    </div>
                    <div className="input-group mb-3">
                        <input
                            className="form-control"
                            // className={ (response !== null && response.data === 'password') ? 'error' : '' }
                            type="password"
                            placeholder={ t('profile.password') }
                            value={ password }
                            onChange={ event => setPassword(event.target.value) }
                            autoComplete="off"
                            required
                        />
                    </div>
                    <div className={ styles.pass_info }>
                        <span style={ password.length >= 6 ? {} : { color: '#e74c3c' } }>
                            <FontAwesomeIcon icon="fa-solid fa-genderless" />
                            &nbsp; { t('profile.passwordTip1') }
                        </span>
                        <span style={ checkPassword(password) ? {} : { color: '#e74c3c' } }>
                            <FontAwesomeIcon icon="fa-solid fa-genderless" />
                            &nbsp; { t('profile.passwordTip2') }
                        </span>
                    </div>
                    <Button
                        type="submit"
                        variant="success"
                    >
                        { t('system.sign_in') }
                    </Button>
                </form>
            </Popup>
        </div>
    )
}
