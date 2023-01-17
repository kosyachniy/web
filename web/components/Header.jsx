import { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import Link from 'next/link'
import { useTranslation } from 'next-i18next'

import { popupSet, searching } from '../redux/actions/system'
import { profileOut } from '../redux/actions/profile'
import { categoriesGet } from '../redux/actions/categories'
import api from '../lib/api'
import styles from '../styles/header.module.css'
import Hexagon from './Hexagon'


export default () => {
    const { t } = useTranslation('common')
    const dispatch = useDispatch()
    const system = useSelector(state => state.system)
    const main = useSelector(state => state.main)
    const online = useSelector(state => state.online)
    const profile = useSelector(state => state.profile)
    const categories = useSelector(state => state.categories)

    const signOut = () => api(main, 'account.exit', {}).then(
        res => dispatch(profileOut(res))
    )

    useEffect(() => {
        if (system.prepared && categories === null) {
            api(main, 'categories.get').then(
                res => dispatch(categoriesGet(res.categories))
            )
        }
    }, [system.prepared, categories])

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
                        <li className="nav-item dropdown">
                            <Link href="/posts/" className="nav-link">
                                { t('structure.posts') }
                            </Link>
                            <ul className="dropdown-menu">
                                { categories && categories.map((category, i) => (
                                    <li key={ i }>
                                        <Link
                                            href={ `/posts/${category.id}/` }
                                            className="dropdown-item"
                                            data-toggle="tooltip"
                                        >
                                            { category.title }
                                        </Link>
                                    </li>
                                )) }
                            </ul>
                        </li>
                        {/* <li className="nav-item">
                            <Link href="/" className="nav-link">
                                { t('structure.space') }
                            </Link>
                        </li> */}
                        {/* <li className="nav-item">
                            <Link href="/room/" className="nav-link">
                                { t('structure.room') }
                            </Link>
                        </li> */}
                        { profile.status >= 6 && (
                            <li className="nav-item">
                                <Link href="/eye/" className="nav-link">
                                    { t('system.admin') }
                                </Link>
                            </li>
                        ) }
                    </ul>
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        <li className="nav-item dropdown">
                            <input
                                className={ `${styles.search} form-control` }
                                type="search"
                                placeholder={ t('system.search') }
                                // value={ system.search }
                                // onChange={ event => dispatch(searching(event.target.value)) }
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
                                        {/* <Link href="/eye/" className="dropdown-item">{ t('system.admin') }</Link> */}
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
