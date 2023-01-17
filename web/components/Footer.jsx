import Link from 'next/link'
import { useSelector, useDispatch } from 'react-redux'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import { changeTheme } from '../redux/actions/main'


export default () => {
    const dispatch = useDispatch()
    const main = useSelector(state => state.main)

    return (
        <footer className={ `bg-${main.theme} ${main.theme === 'dark' ? "" : "text-muted"} pt-3` }>
            <div className="container d-flex flex-wrap justify-content-between align-items-center py-3 mt-4 border-top">
                <p className="col-md-4 mb-0">
                    { process.env.NEXT_PUBLIC_NAME } &copy; 2018-{ new Date().getFullYear() }
                </p>
                <Link href="/" className="col-md-4 d-flex align-items-center justify-content-center mb-md-0 me-md-auto link-dark text-decoration-none">
                    <img
                        src={ `/brand/logo_${main.color}.svg` }
                        alt={ process.env.NEXT_PUBLIC_NAME }
                        style={{ height: '24px' }}
                    />
                </Link>
                <ul className="nav col-md-4 justify-content-end list-unstyled d-flex">
                    <li
                        className="ms-3"
                        style={{ cursor: 'pointer' }}
                        onClick={ () => dispatch(changeTheme(main.theme === 'dark' ? 'light' : 'dark')) }
                    >
                        { main.theme === 'dark' ? (
                            <FontAwesomeIcon icon="fa-solid fa-sun" />
                            // fa-sun-bright
                        ) : (
                            <FontAwesomeIcon icon="fa-solid fa-moon" />
                        ) }
                    </li>
                    <Link
                        href='/'
                        locale={ main.locale === 'ru' ? 'en' : 'ru' }
                    >
                        <li
                            className="ms-3 d-flex"
                            style={{ cursor: 'pointer' }}
                            // onClick={ () => dispatch(changeLang(main.locale === 'ru' ? 'en' : 'ru')) }
                        >
                            <img
                                src={ `/lang/${main.locale}.svg` }
                                alt={ main.locale }
                                style={{ height: '24px' }}
                            />
                        </li>
                    </Link>
                </ul>
            </div>
        </footer>
    )
}
