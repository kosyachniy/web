import { useSelector, useDispatch } from 'react-redux'
import Link from 'next/link'
import { useRouter } from 'next/router'
import { useTranslation } from 'next-i18next'

import { popupSet, searching } from '../redux/actions/system'
import { profileOut } from '../redux/actions/profile'
import api from '../lib/api'
import styles from '../styles/header.module.css'
import Hexagon from './Hexagon'


const Logo = () => {
    const main = useSelector(state => state.main)

    return (
        <Link href="/" className="navbar-brand">
            <img
                src={ `/brand/logo_${main.color}.svg` }
                alt={ process.env.NEXT_PUBLIC_NAME }
            />
        </Link>
    )
}

const Navigation = () => {
    const { t } = useTranslation('common')
    const main = useSelector(state => state.main)
    const categories = useSelector(state => state.categories)

    return (
        <>
            <li className="nav-item dropdown">
                <Link href="/posts/" className="nav-link">
                    { t('structure.posts') }
                </Link>
                <ul className={ `${styles.menu} dropdown-menu dropdown-menu-${main.theme}` }>
                    { categories && categories.map(category => category.id ? (
                        <Link
                            href={ `/posts/${category.id}/` }
                            className="dropdown-item"
                            key={ category.id }
                        >
                            { category.title }
                        </Link>
                    ) : (<></>)) }
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
        </>
    )
}

const Search = () => {
    const { t } = useTranslation('common')
    const dispatch = useDispatch()
    const router = useRouter()
    const system = useSelector(state => state.system)

    const search = value => {
        dispatch(searching(value))
        router.push("/posts/")
    }

    return (
        <input
            className={ `${styles.search} form-control` }
            type="search"
            placeholder={ t('system.search') }
            value={ system.search }
            onChange={ event => search(event.target.value) }
        />
    )
}

const Online = () => {
    const { t } = useTranslation('common')
    const dispatch = useDispatch()
    const online = useSelector(state => state.online)

    if (!online.count) {
        return (
            <div>
                { t('system.offline') }
                <div className={ styles.offline }></div>
            </div>
        )
    }

    return (
        <div>
            { t('system.online') }
            <div className={ styles.online }></div>
            <div
                className="badge bg-secondary"
                onClick={ () => dispatch(popupSet('online')) }
            >{ online.count } </div>
        </div>
    )
}

const Profile = () => {
    const { t } = useTranslation('common')
    const dispatch = useDispatch()
    const main = useSelector(state => state.main)
    const profile = useSelector(state => state.profile)

    const signOut = () => api(main, 'account.exit', {}).then(
        res => dispatch(profileOut(res))
    )

    if (!profile.id) {
        return (
            <div style={{ paddingRight: 0, paddingBottom: 0 }}>
                <button
                    type="button"
                    className="btn btn-success"
                    onClick={ () => dispatch(popupSet('auth')) }
                >{ t('system.sign_in') }</button>
            </div>
        )
    }

    return (
        <>
            <div
                className="nav-link"
                id="navbarDropdown"
                data-bs-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
                style={{ padding: 0 }}
            >
                <Hexagon url={ profile.image_optimize } />
            </div>
            <ul
                id="profile"
                className={ `${styles.menu} dropdown-menu dropdown-menu-end dropdown-menu-${main.theme}` }
                aria-labelledby="navbarDropdown"
            >
                <Link href="/profile/" className="dropdown-item">
                    { t('system.profile') }
                </Link>
                {/* <Link href="/settings/" className="dropdown-item">
                    { t('system.settings') }
                </Link> */}
                {/* <Link href="/analytics/" className="dropdown-item">
                    { t('system.analytics') }
                </Link> */}
                {/* <Link href="/billing/" className="dropdown-item">
                    { t('system.billing') }
                </Link> */}
                { profile.status >= 6 && (
                    <Link href="/eye/" className="dropdown-item">
                        { t('system.admin') }
                    </Link>
                ) }
                <div className="dropdown-item" onClick={ signOut }>
                    { t('system.sign_out') }
                </div>
            </ul>
        </>
    )
}

export default () => {
    const main = useSelector(state => state.main)

    return (
        <nav className={ `navbar sticky-top navbar-expand-lg navbar-${main.theme} bg-${main.theme}` }>
            <div className="container">
                <Logo />
                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#burger"
                    aria-controls="burger"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="burger">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        <Navigation />
                    </ul>
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        <li className="nav-item">
                            <Search />
                        </li>
                    </ul>
                    <ul className="nav navbar-nav navbar-right">
                        <li className="nav-item">
                            <Online />
                        </li>
                        <li className="nav-item dropdown">
                            <Profile />
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    )
}
