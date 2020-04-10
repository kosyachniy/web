import React from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

import './style.css'
import { name } from '../../../sets'


// const sciences = [
// 	'math', 'prog', 'bis', 'manag', 'lead', 'marketing', 'life_safety'
// ]

const events = [
	'hack', 'meet', 'lect', 'pres'
]

const link = 'https://tensy.org/load/users/0.png';


export default function Header(props) {
	const {
		system, online, profile,
		changeTheme,
		handlerLogIn,
	} = props
	const { t } = useTranslation()

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
					</ul>
					<ul className="navbar-nav mr-auto mt-2 mt-lg-0">
						<li className="nav-item">
							<form action="/search/" method="post" className="form-inline my-2 my-lg-0">
								<input name="search" className="form-control mr-sm-2" type="search" placeholder={ t('system.search') } />
							</form>
						</li>
					</ul>
					<ul className="nav navbar-nav navbar-right">
						<li className="nav-item">
							<div>
								{ online.count ? (
									<>
										{t('system.online')}
										<div className="online"></div>
										<div className="badge badge-secondary">{ online.count } </div>
									</>
								) : (
									<>
										{t('system.offline')}
										<div className="offline"></div>
									</>
								) }
							</div>
						</li>
						<li className="nav-item">
							{system.theme === 'dark' ? (
								<div className="badge" onClick={() => {changeTheme('light')}}>
									<i className="fas fa-sun" />
								</div>
							) : (
								<div className="badge" onClick={() => {changeTheme('dark')}}>
									<i className="fas fa-moon" />
								</div>
							)}
						</li>
						<li className="nav-item">
							{localStorage.getItem('lang') === 'ru' ? (
								<div className="badge" onClick={ () => {props.handlerLang('en')} }>
									<img src="/lang/en.svg" alt="en" />
								</div>
							) : (
								<div className="badge" onClick={ () => {props.handlerLang('ru')} }>
									<img src="/lang/ru.svg" alt="ru" />
								</div>
							)}
						</li>
						<li className="nav-item">
							{profile.id ? (
								<div className="hexagon">
									<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1">
										<path d="M0.5,0.0005C0.475,0.0005,0.4495,0.005,0.4255,0.0145c-0.038,0.0145-0.091,0.039-0.159,0.0785c-0.068,0.0395-0.1155,0.0735-0.147,0.0994 C0.08,0.2245,0.0535,0.2705,0.0455,0.3215c-0.0065,0.0405-0.012,0.099-0.012,0.179c0,0.079,0.0055,0.1375,0.012,0.178c0.008,0.0515,0.0345,0.0969,0.0745,0.1295 c0.032,0.026,0.079,0.06,0.147,0.0994c0.068,0.0395,0.1215,0.064,0.1595,0.079c0.048,0.0185,0.1005,0.0185,0.148-0.0005c0.038-0.0145,0.091-0.039,0.159-0.079c0.068-0.0395,0.1155-0.0735,0.147-0.0994c0.0395-0.0325,0.0665-0.0785,0.0745-0.1295c0.0065-0.0405,0.012-0.099,0.012-0.179c-0.0005-0.079-0.006-0.1369-0.012-0.178c-0.008-0.0515-0.0345-0.0969-0.0745-0.1295c-0.032-0.026-0.079-0.06-0.147-0.0994C0.665,0.053,0.612,0.0285,0.574,0.0139C0.55,0.005,0.525,0.0005,0.5,0.0005z" fill={`url(#${link})`} />
										<defs>
											<pattern id={link} x="0" y="0" width="1" height="1" viewBox="0 0 1 1">
												<rect x="0" y="-0.035" />
												<image xlinkHref={link} x="-0.035" width="1.07" height="1.07" y="-0.035" preserveAspectRatio="xMidYMid slice" />
											</pattern>
										</defs>
									</svg>
								</div>
							) : (
								<div>
									<button
										type="button"
										class="btn btn-success"
										onClick={ ()=>{handlerLogIn(true)} }
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