import React from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

import './style.css'
import { name } from '../../../sets'


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
							<div className="dropdown-content">
								<Link to="/posts/math/" data-toggle="tooltip">Математика</Link>
								<Link to="/posts/prog/" data-toggle="tooltip">Программирование</Link>
								<Link to="/posts/bis/" data-toggle="tooltip">Бизнес и экономика</Link>
								<Link to="/posts/manag/" data-toggle="tooltip">Менеджмент</Link>
								<Link to="/posts/lead/" data-toggle="tooltip">Харизма и лидерство</Link>
								<Link to="/posts/xxx/" data-toggle="tooltip">Выживание</Link>
								<Link to="/posts/yyy/" data-toggle="tooltip">Маркетинг</Link>
							</div>
						</li>
						<li className="nav-item dropdown">
							<Link to="/events/" className="nav-link">{ t('structure.events') }</Link>
							<div className="dropdown-content">
								<Link to="/events/hacks/" data-toggle="tooltip">Соревнования</Link>
								<Link to="/events/meet/" data-toggle="tooltip">Митапы</Link>
								<Link to="/events/lect/" data-toggle="tooltip">Лекции</Link>
								<Link to="/events/pres/" data-toggle="tooltip">Презентации</Link>
							</div>
						</li>
					</ul>
					<ul className="nav navbar-nav navbar-right">
						<li className="nav-item dropdown">	
							<form action="/search/" method="post" className="form-inline my-2 my-lg-0">
								<input name="search" className="form-control mr-sm-2" type="search" placeholder="Поиск" />
							</form>
						</li>
						<li className="nav-item">
							<Link to="/user/"className="nav-link">Логин</Link><Link to="/sys_sign_out/" className="nav-link">Выйти</Link>
							{/* <Link to="/login/" className="nav-link">Гость &nbsp; Войти</Link> */}
						</li>
					</ul>
				</div>
			</div>
		</nav>
	)
}