import React from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

import api from '../../../lib/api'

import './style.css'

import Hexagon from '../../../components/Hexagon'


// const sciences = [
//     'math', 'prog', 'bis', 'manag', 'lead', 'marketing', 'life_safety'
// ]

// const events = [
//     'hack', 'meet', 'lect', 'pres'
// ]


const Header = (props) => {
    const {
        system, online, profile,
        profileOut,
        handlerPopUp, searching,
    } = props
    const { t } = useTranslation()

    const signOut = () => {
        api('account.exit', {}).then(res => {
            profileOut(res)
        })
    }

    return (
        <nav className={`navbar sticky-top navbar-expand-lg navbar-${system.theme} bg-${system.theme}`}>
            <div className="container">
                <Link to="/" className="navbar-brand"><img src={`/brand/logo_${system.color}.svg`} alt={ process.env.REACT_APP_NAME } /></Link>
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
                            <Link to="/feed/" className="nav-link">{ t('structure.feed') }</Link>
                        </li> */}
                        <li className="nav-item dropdown">
                            <Link to="/posts/" className="nav-link">{ t('structure.posts') }</Link>
                            {/* <Link to="/admin/add/ladder/"><span className="badge badge-dark">+</span></Link> */}
                            {/* <div className="dropdown-content">
                                {
                                    sciences.map((science) => (
                                        <Link to={ `/posts/${science}/` } data-toggle="tooltip">{ t(`science.${science}`) }</Link>
                                    ))
                                }
                            </div> */}
                        </li>
                        {/* <li className="nav-item">
                            <Link to="/" className="nav-link">{ t('structure.space') }</Link>
                        </li> */}
                        <li className="nav-item">
                            <Link to="/room/" className="nav-link">{ t('structure.room') }</Link>
                        </li>
                        {/* <li className="nav-item dropdown">
                            <Link to="/events/" className="nav-link">{ t('structure.events') }</Link>
                            <div className="dropdown-content">
                                {
                                    events.map((event, ind) => (
                                        <Link
                                            to={ `/events/${event}/` }
                                            data-toggle="tooltip"
                                            key={ ind }
                                        >{ t(`events.${event}`) }</Link>
                                    ))
                                }
                            </div>
                        </li> */}
                        {/* <li className="nav-item">
                            <Link to="/map/" className="nav-link">{ t('structure.map') }</Link>
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
                                onChange={ (event) => {searching(event.target.value)} }
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
                                        onClick={ ()=>{handlerPopUp('online')} }
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
                                        <Link className="dropdown-item" to="/profile/">{t('system.profile')}</Link>
                                        {/* <Link className="dropdown-item" to="/settings/">{t('system.settings')}</Link> */}
                                        {/* <Link className="dropdown-item" to="/analytics/">{t('system.analytics')}</Link> */}
                                        {/* <Link className="dropdown-item" to="/admin/">{t('system.admin')}</Link> */}
                                        <div className="dropdown-item" onClick={ signOut }>{t('system.sign_out')}</div>
                                    </div>
                                </>
                            ) : (<></>)}
                            {!profile.id ? (
                                <div style={ {paddingRight: 0, paddingBottom: 0} }>
                                    <button
                                        type="button"
                                        className="btn btn-success"
                                        onClick={ ()=>{handlerPopUp('auth')} }
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

export default Header;
