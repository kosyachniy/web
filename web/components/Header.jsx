import Link from 'next/link'
import { useTranslation } from 'next-i18next'
import { useSelector, useDispatch } from 'react-redux'

import { popupSet, searching } from '../redux/actions/system'
import { profileOut } from '../redux/actions/profile'
import api from '../functions/api'
import styles from '../styles/header.module.css'
import Hexagon from './Hexagon'


// const sciences = [
//     'math', 'prog', 'bis', 'manag', 'lead', 'marketing', 'life_safety'
// ]

// const events = [
//     'hack', 'meet', 'lect', 'pres'
// ]


export default () => {
    const { t } = useTranslation('common')
    const dispatch = useDispatch()
    const main = useSelector((state) => state.main)
    const online = useSelector((state) => state.online)
    const profile = useSelector((state) => state.profile)

    const signOut = () => {
        api(main.token, main.locale, 'account.exit', {}).then(res => {
            dispatch(profileOut(res))
        })
    }

    return (
        <nav className={ `navbar sticky-top navbar-expand-lg navbar-${main.theme} bg-${main.theme}` }>
            <div className="container">
                <Link href="/" className="navbar-brand"><img src={ `/brand/logo_${main.color}.svg` } alt={ process.env.NEXT_PUBLIC_NAME } /></Link>
                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarTogglerDemo02"
                    aria-controls="navbarTogglerDemo02"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarTogglerDemo02">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        {/* <li className="nav-item">
                            <Link href="/feed/" className="nav-link">{ t('structure.feed') }</Link>
                        </li> */}
                        <li className="nav-item dropdown">
                            <Link href="/posts/" className="nav-link">{ t('structure.posts') }</Link>
                            {/* <Link href="/admin/add/ladder/"><span className="badge badge-dark">+</span></Link> */}
                            {/* <div className="dropdown-content">
                                {
                                    sciences.map((science) => (
                                        <Link href={ `/posts/${science}/` } data-toggle="tooltip">{ t(`science.${science}`) }</Link>
                                    ))
                                }
                            </div> */}
                        </li>
                        {/* <li className="nav-item">
                            <Link href="/" className="nav-link">{ t('structure.space') }</Link>
                        </li> */}
                        <li className="nav-item">
                            <Link href="/room/" className="nav-link">{ t('structure.room') }</Link>
                        </li>
                        {/* <li className="nav-item dropdown">
                            <Link href="/events/" className="nav-link">{ t('structure.events') }</Link>
                            <div className="dropdown-content">
                                {
                                    events.map((event, ind) => (
                                        <Link
                                            href={ `/events/${event}/` }
                                            data-toggle="tooltip"
                                            key={ ind }
                                        >{ t(`events.${event}`) }</Link>
                                    ))
                                }
                            </div>
                        </li> */}
                        {/* <li className="nav-item">
                            <Link href="/map/" className="nav-link">{ t('structure.map') }</Link>
                        </li> */}
                    </ul>
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        <li className="nav-item dropdown">
                            <input
                                className={ `${styles.search} form-control` }
                                type="search"
                                placeholder={ t('system.search') }
                                // value={ system.search }
                                // onChange={ (event) => dispatch(searching(event.target.value)) }
                            />
                        </li>
                    </ul>
                    <ul className="nav navbar-nav navbar-right">
                        <li className="nav-item">
                            { online.count ? (
                                <div>
                                    { t('system.online') }
                                    <div className={ styles.online }></div>
                                    <div
                                        className="badge bg-secondary"
                                        onClick={ () => dispatch(popupSet('online')) }
                                    >{ online.count } </div>
                                </div>
                            ) : (
                                <div>
                                    { t('system.offline') }
                                    <div className={ styles.offline }></div>
                                </div>
                            ) }
                        </li>
                        <li className="nav-item dropdown">
                            { profile.id ? (
                                <>
                                    <div
                                        id="navbarDropdown"
                                        className="nav-link"
                                        data-bs-toggle="dropdown"
                                        aria-haspopup="true"
                                        aria-expanded="false"
                                        style={{ padding: 0 }}
                                    >
                                        <Hexagon url={ profile.image_optimize } />
                                    </div>
                                    <div
                                        className={ `${styles.menu} dropdown-menu dropdown-menu-end dropdown-menu-${main.theme}` }
                                        aria-labelledby="navbarDropdown"
                                    >
                                        <Link href="/profile/" className="dropdown-item">{ t('system.profile') }</Link>
                                        {/* <Link href="/settings/" className="dropdown-item">{ t('system.settings') }</Link> */}
                                        {/* <Link href="/analytics/" className="dropdown-item">{ t('system.analytics') }</Link> */}
                                        {/* <Link href="/admin/" className="dropdown-item">{ t('system.admin') }</Link> */}
                                        <div className="dropdown-item" onClick={ signOut }>{ t('system.sign_out') }</div>
                                    </div>
                                </>
                            ) : (<></>) }
                            { !profile.id ? (
                                <div style={{ paddingRight: 0, paddingBottom: 0 }}>
                                    <button
                                        type="button"
                                        className="btn btn-success"
                                        onClick={ () => dispatch(popupSet('auth')) }
                                    >{ t('system.sign_in') }</button>
                                </div>
                            ) : (<></>) }
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    )
}
