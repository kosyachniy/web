import { useSelector, useDispatch } from 'react-redux'

import { popupSet } from '../../redux/actions/system'
import styles from '../../styles/auth.module.css'
import Popup from '../Popup'


export default () => {
    const dispatch = useDispatch()
    const main = useSelector(state => state.main)

    return (
        <div className={ styles.auth }>
            <Popup theme={ main.theme } >
                <button
                    className={ styles.btn_mail }
                    onClick={ () => dispatch(popupSet('mail')) }
                >
                    <i className="bi bi-envelope-fill" />
                </button>
                <button
                    href={ `https://oauth.vk.com/authorize?client_id=${process.env.NEXT_PUBLIC_VK_ID}&display=popup&redirect_uri=${process.env.NEXT_PUBLIC_WEB}callback&scope=4194304&response_type=code&v=5.103` }
                    className={ styles.btn_vk }
                    onClick={ () => localStorage.setItem('previousPath', document.location.href) }
                >
                    <i className="fa-brands fa-vk" />
                </button>
                <button
                    href={ `https://accounts.google.com/o/oauth2/auth?redirect_uri=${process.env.NEXT_PUBLIC_WEB}callback&response_type=code&client_id=${process.env.NEXT_PUBLIC_GOOGLE_ID}&scope=https://www.googleapis.com/auth/userinfo.email%20https://www.googleapis.com/auth/userinfo.profile` }
                    className={ styles.btn_g }
                    onClick={ () => localStorage.setItem('previousPath', document.location.href) }
                >
                    <i className="fa-brands fa-google" />
                </button>
                <button
                    href={ `https://t.me/retestme?start=<token>` }
                    target="_blank"
                    rel="noopener noreferrer"
                    className={ styles.btn_tg }
                    onClick={ () => localStorage.setItem('previousPath', document.location.href) }
                >
                    <i className="fa-brands fa-telegram" />
                </button>
            </Popup>
        </div>
    )
}
