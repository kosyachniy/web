import Link from 'next/link'
import { useRouter } from 'next/router'
import { useSelector, useDispatch } from 'react-redux'

import { changeLang, changeTheme } from '../store'


export default () => {
    const dispatch = useDispatch()
    const router = useRouter()
    const system = useSelector((state) => state.system)

    return (
        <footer className={ `bg-${system.theme} ${system.theme === 'dark' ? "" : "text-muted"} pt-3` }>
            <div className="container d-flex flex-wrap justify-content-between align-items-center py-3 mt-4 border-top">
                <p className="col-md-4 mb-0">
                    { process.env.NEXT_PUBLIC_NAME } &copy; 2018-{ new Date().getFullYear() }
                </p>
                <Link href="/" className="col-md-4 d-flex align-items-center justify-content-center mb-md-0 me-md-auto link-dark text-decoration-none">
                    <img
                        src={ `/brand/logo_${system.color}.svg` }
                        alt={ process.env.NEXT_PUBLIC_NAME }
                        style={{ height: '24px' }}
                    />
                </Link>
                <ul className="nav col-md-4 justify-content-end list-unstyled d-flex">
                    <li
                        id="theme"
                        className="ms-3 u-cursor"
                        onClick={ () => dispatch(changeTheme(system.theme === 'dark' ? 'light' : 'dark')) }
                    >
                        <i className={ `bi ${system.theme === 'dark' ? "bi-sun-fill" : "bi-moon-fill"}` } />
                    </li>
                    <li
                        id="lang"
                        className="ms-3 d-flex u-cursor"
                        onClick={ () => dispatch(changeLang(system.locale === 'ru' ? 'en' : 'ru')) }
                    >
                        <img
                            src={ `/lang/${system.locale === 'ru' ? 'en' : 'ru'}.svg` }
                            alt={ system.locale === 'ru' ? 'en' : 'ru' }
                            style={{ height: '24px' }}
                        />
                    </li>
                </ul>
            </div>
        </footer>
    )
}
