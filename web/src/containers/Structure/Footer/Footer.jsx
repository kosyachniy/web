import React from 'react'
// import { Link } from 'react-router-dom'
// import { useTranslation } from 'react-i18next'

import './style.css'
import { name } from '../../../sets'


const Footer = (props) => {
    const { system, changeLang, changeTheme } = props
    // const { t } = useTranslation()

    return (
        <footer className={`section footer-classic context-${system.theme} bg-${system.theme}`}>
            <div className="container">
                <div className="row">
                    <div className="col">
                        <p className="rights">
                            { name } © 2018-{ new Date().getFullYear() }
                        </p>
                    </div>
                    <div className="col text-right">
                        <p>
                            {system.theme === 'dark' ? (
                                <div id="theme" className="badge" onClick={() => {changeTheme('light')}}>
                                    <i className="fas fa-sun" />
                                </div>
                            ) : (
                                <div id="theme" className="badge" onClick={() => {changeTheme('dark')}}>
                                    <i className="fas fa-moon" />
                                </div>
                            )}
                            &nbsp;|&nbsp;
                            {system.locale === 'ru' ? (
                                <div id="lang" className="badge" onClick={ () => {changeLang('en')} }>
                                    <img src="/lang/en.svg" alt="en" />
                                </div>
                            ) : (
                                <div id="lang" className="badge" onClick={ () => {changeLang('ru')} }>
                                    <img src="/lang/ru.svg" alt="ru" />
                                </div>
                            )}
                            {/* <Link to="/about/">{ t('footer.about') }</Link> */}
                            {/* <div className="social">
                                { social.map((el, num) =>
                                    <a href={ el.cont } key={ num }><span className="badge"><img src={ '/social/' + el.name + '.ico' } alt={ el.name } /></span></a>
                                ) }
                            </div> */}
                        </p>
                    </div>
                </div>
            </div>
        </footer>
    )
}

export default Footer;
