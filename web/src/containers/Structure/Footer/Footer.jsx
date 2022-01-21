import React from 'react'
// import { Link } from 'react-router-dom'
// import { useTranslation } from 'react-i18next'

import './style.css'


const Footer = (props) => {
    const { system, changeLang, changeTheme } = props
    // const { t } = useTranslation()

    return (
        <footer className={`bg-${system.theme}`}>
            <div className="container d-flex flex-wrap justify-content-between align-items-center py-3 mt-4 border-top">
                <div className="col-md-4 d-flex align-items-center">
                    { process.env.REACT_APP_NAME } &copy; 2018-{ new Date().getFullYear() }
                </div>
                <ul
                    className="nav col-md-4 justify-content-end list-unstyled d-flex"
                    style={{ lineHeight: '1.2em' }}
                >
                    <li
                        id="theme"
                        className="ms-3 u-cursor"
                        onClick={() => {
                            changeTheme(system.theme === 'dark' ? 'light' : 'dark')
                        }}
                    >
                        <a><i className={`fas ${system.theme === 'dark' ? "fa-sun" : "fa-moon"}`} /></a>
                    </li>
                    <li
                        className="ms-3 text-muted"
                        style={{ height: '1em', lineHeight: '1em' }}
                    >
                        |
                    </li>
                    <li
                        id="lang"
                        className="ms-3 u-cursor"
                        onClick={ () => {changeLang(system.locale === 'ru' ? 'en' : 'ru')} }
                        style={{ height: '1em', lineHeight: '1em' }}
                    >
                        <img
                            src={`/lang/${system.locale === 'ru' ? "en" : "ru"}.svg`}
                            alt={system.locale === 'ru' ? "en" : "ru"}
                            style={{ height: '1em' }}
                        />
                    </li>
                    {/* <Link to="/about/">{ t('footer.about') }</Link> */}
                    {/* <div className="social">
                        { social.map((el, num) =>
                            <a href={ el.data } key={ num }><span className="badge"><img src={ '/social/' + el.title + '.ico' } alt={ el.title } /></span></a>
                        ) }
                    </div> */}
                </ul>
            </div>
        </footer>
    )
}

export default Footer;
