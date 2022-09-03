import Link from 'next/link'
import { useTranslation } from 'next-i18next'
import { useSelector, useDispatch } from 'react-redux'

import { popupSet, profileOut, searching } from '../store'
import api from '../functions/api'
// import styles from '../styles/header.module.css'
import Hexagon from './Hexagon'


// const sciences = [
//     'math', 'prog', 'bis', 'manag', 'lead', 'marketing', 'life_safety'
// ]

// const events = [
//     'hack', 'meet', 'lect', 'pres'
// ]


export default () => {
    const dispatch = useDispatch()
    const system = useSelector((state) => state.system)
    const online = useSelector((state) => state.online)
    const profile = useSelector((state) => state.profile)
    // const dispatch = useDispatch()

    const { t } = useTranslation()

    const signOut = () => {
        api('account.exit', {}).then(res => {
            // () => dispatch(profileOut(res))
        })
    }

    return (
        <nav className={`navbar sticky-top navbar-expand-lg navbar-${system.theme} bg-${system.theme}`}>
            <div className="container">
                <Link href="/"><a className="navbar-brand"><img src={`/brand/logo_${system.color}.svg`} alt={ process.env.NEXT_PUBLIC_NAME } /></a></Link>
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
                            <Link href="/feed/"><a className="nav-link">{ t('structure.feed') }</a></Link>
                        </li> */}
                        <li className="nav-item dropdown">
                            <Link href="/posts/"><a className="nav-link">{ t('structure.posts') }</a></Link>
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
                            <Link href="/"><a className="nav-link">{ t('structure.space') }</a></Link>
                        </li> */}
                        <li className="nav-item">
                            <Link href="/room/"><a className="nav-link">{ t('structure.room') }</a></Link>
                        </li>
                        {/* <li className="nav-item dropdown">
                            <Link href="/events/"><a className="nav-link">{ t('structure.events') }</a></Link>
                            <div className="dropdown-content">
                                {
                                    events.map((event, ind) => (
                                        <Link href={ `/events/${event}/` }><a
                                            data-toggle="tooltip"
                                            key={ ind }
                                        >{ t(`events.${event}`) }</a></Link>
                                    ))
                                }
                            </div>
                        </li> */}
                        {/* <li className="nav-item">
                            <Link href="/map/"><a className="nav-link">{ t('structure.map') }</a></Link>
                        </li> */}
                    </ul>
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        <li className="nav-item dropdown">
                            <input
                                id="search"
                                className="form-control"
                                type="search"
                                placeholder={ t('system.search') }
                                value={ system.search }
                                // onChange={ (event) => dispatch(searching(event.target.value)) }
                            />
                        </li>
                    </ul>
                    <ul className="nav navbar-nav navbar-right">
                        <li className="nav-item">
                            { online.count ? (
                                <div>
                                    {t('system.online')}
                                    <div className="online"></div>
                                    <div
                                        className="badge bg-secondary"
                                        onClick={ () => dispatch(popupSet('online')) }
                                    >{ online.count } </div>
                                </div>
                            ) : (
                                <div>
                                    {t('system.offline')}
                                    <div className="offline"></div>
                                </div>
                            ) }
                        </li>
                        <li className="nav-item dropdown">
                            {profile.id ? (
                                <>
                                    <div
                                        id="navbarDropdown"
                                        className="nav-link"
                                        data-bs-toggle="dropdown"
                                        aria-haspopup="true"
                                        aria-expanded="false"
                                        style={ {padding: 0} }
                                    >
                                        <Hexagon url={ profile.avatar_optimize } />
                                    </div>
                                    <div
                                        id="menu"
                                        className={`dropdown-menu dropdown-menu-end dropdown-menu-${system.theme}`}
                                        aria-labelledby="navbarDropdown"
                                    >
                                        <Link href="/profile/"><a className="dropdown-item">{t('system.profile')}</a></Link>
                                        {/* <Link href="/settings/"><a className="dropdown-item">{t('system.settings')}</a></Link> */}
                                        {/* <Link href="/analytics/"><a className="dropdown-item">{t('system.analytics')}</a></Link> */}
                                        {/* <Link href="/admin/"><a className="dropdown-item">{t('system.admin')}</a></Link> */}
                                        <div className="dropdown-item" onClick={ signOut }>{t('system.sign_out')}</div>
                                    </div>
                                </>
                            ) : (<></>)}
                            {!profile.id ? (
                                <div style={ {paddingRight: 0, paddingBottom: 0} }>
                                    <button
                                        type="button"
                                        className="btn btn-success"
                                        onClick={ () => dispatch(popupSet('auth')) }
                                    >{ t('system.sign_in') }</button>
                                </div>
                            ) : (<></>)}
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    )
}
