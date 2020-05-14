import React from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

import api from '../../../func/api'

import './style.css'
import { name } from '../../../sets'

import Hexagon from '../../../components/Hexagon'


// const sciences = [
// 	'math', 'prog', 'bis', 'manag', 'lead', 'marketing', 'life_safety'
// ]

// const events = [
// 	'hack', 'meet', 'lect', 'pres'
// ]


export default function Header(props) {
	const {
		system, online, profile,
		changeTheme, changeLang, profileOut,
		handlerPopUp,
	} = props
	const { t } = useTranslation()

	const signOut = () => {
		const handlerSuccess = res => {
			profileOut(res)
		}

		api('account.exit', {}, handlerSuccess)
	}

	return (
		<nav className={`navbar navbar-expand-lg navbar-${system.theme} bg-${system.theme} sticky-top`}>
			<div className="container">
				<Link to="/" className="navbar-brand"><img src={`/brand/logo_${system.color}.svg`} alt={ name } /></Link>
				<button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
					<span className="navbar-toggler-icon"></span>
				</button>

				<div className="collapse navbar-collapse" id="navbarTogglerDemo02">
					<ul className="navbar-nav mr-auto mt-2 mt-lg-0">
						<li className="nav-item">
							<Link to="/" className="nav-link">{ t('structure.space') }</Link>
						</li>
						<li className="nav-item">
							<Link to="/feed/" className="nav-link">{ t('structure.feed') }</Link>
						</li>
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
						<li className="nav-item">
							<Link to="/map/" className="nav-link">{ t('structure.map') }</Link>
						</li>
					</ul>
					<ul className="navbar-nav mr-auto mt-2 mt-lg-0">
						<li className="nav-item">
							<input
								id="search"
								className="form-control"
								type="search"
								placeholder={ t('system.search') }
							/>
						</li>
					</ul>
					<ul className="nav navbar-nav navbar-right">
						<li className="nav-item">
							<div>
								{ online.count && (
									<>
										{t('system.online')}
										<div className="online"></div>
										<div
											className="badge badge-secondary"
											onClick={ ()=>{handlerPopUp('online'); console.log('online')} }
										>{ online.count } </div>
									</>
								) || (
									<>
										{t('system.offline')}
										<div className="offline"></div>
									</>
								) }
							</div>
						</li>
						<li className="nav-item">
							{system.theme === 'dark' && (
								<div id="theme" className="badge" onClick={() => {changeTheme('light')}}>
									<i className="fas fa-sun" />
								</div>
							) || (
								<div id="theme" className="badge" onClick={() => {changeTheme('dark')}}>
									<i className="fas fa-moon" />
								</div>
							)}
						</li>
						<li className="nav-item">
							{system.lang === 'ru' && (
								<div id="lang" className="badge" onClick={ () => {changeLang('en')} }>
									<img src="/lang/en.svg" alt="en" />
								</div>
							) || (
								<div id="lang" className="badge" onClick={ () => {changeLang('ru')} }>
									<img src="/lang/ru.svg" alt="ru" />
								</div>
							)}
						</li>
						<li className="nav-item dropdown">
							{profile.id && (
								<>
									<div
										className="nav-link"
										data-toggle="dropdown"
										aria-haspopup="true"
										aria-expanded="false"
										style={ {padding: 0} }
									>
										<Hexagon url={ profile.avatar } />
									</div>
									<div className="dropdown-menu dropdown-menu-right" id="menu">
										<Link className="dropdown-item" to="/profile/">{t('system.profile')}</Link>
										<Link className="dropdown-item" to="/settings/">{t('system.settings')}</Link>
										<Link className="dropdown-item" to="/analytics/">{t('system.analytics')}</Link>
										<Link className="dropdown-item" to="/admin/">{t('system.admin')}</Link>
										<div className="dropdown-item" onClick={ signOut }>{t('system.sign_out')}</div>
									</div>
								</>
							) || (
								<div>
									<button
										type="button"
										className="btn btn-success"
										onClick={ ()=>{handlerPopUp('auth')} }
									>{ t('system.sign_in') }</button>
								</div>
							)}
						</li>
					</ul>
				</div>
			</div>
		</nav>
	)
}