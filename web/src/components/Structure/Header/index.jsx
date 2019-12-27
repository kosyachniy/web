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


export default function Header() {
	const { t } = useTranslation()

	return (
		<nav className="navbar navbar-expand-lg navbar-light bg-light sticky-top">
			<div className="container">
				<Link to="/" className="navbar-brand"><img src="/brand/logo.svg" alt={ name } /></Link>
				<button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
					<span className="navbar-toggler-icon"></span>
				</button>

				<div className="collapse navbar-collapse" id="navbarTogglerDemo02">
					<ul className="navbar-nav mr-auto mt-2 mt-lg-0">
						<li className="nav-item">
							<Link to="/" className="nav-link">{ t('structure.space') }</Link>
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
						<li className="nav-item dropdown">
							<Link to="/events/" className="nav-link">{ t('structure.events') }</Link>
							<div className="dropdown-content">
								{
									events.map((event) => (
										<Link to={ `/events/${event}/` } data-toggle="tooltip">{ t(`events.${event}`) }</Link>
									))
								}
							</div>
						</li>
					</ul>
					<ul className="nav navbar-nav navbar-right">
						<li className="nav-item dropdown">	
							<form action="/search/" method="post" className="form-inline my-2 my-lg-0">
								<input name="search" className="form-control mr-sm-2" type="search" placeholder={ t('system.search') } />
							</form>
						</li>
						<li className="nav-item">
							<Link to="/user/"className="nav-link">@</Link><Link to="/sys_sign_out/" className="nav-link">{ t('system.sign_out') }</Link>
							{/* <Link to="/login/" className="nav-link">Гость &nbsp; { t('system.sign_in') }</Link> */}
						</li>
					</ul>
				</div>
			</div>
		</nav>
	)
}