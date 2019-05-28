import React from 'react'

import './style.css'
import { name } from '../../sets'


export default function Header() {
	return (
		<nav className="navbar navbar-expand-lg navbar-light bg-light sticky-top">
			<div className="container">
				<a href="/" className="navbar-brand"><img src="/brand/logo.svg" alt={ name } /></a>
				<button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
					<span className="navbar-toggler-icon"></span>
				</button>

				<div className="collapse navbar-collapse" id="navbarTogglerDemo02">
					<ul className="navbar-nav mr-auto mt-2 mt-lg-0">
						<li className="nav-item dropdown">
							<a href="/learn/" className="nav-link">Посты</a>
							{/* <a href="/admin/add/ladder/"><span className="badge badge-dark">+</span></a> */}
							<div className="dropdown-content">
								<a href="/learn/ladders/" data-toggle="tooltip">Программирование</a>
								<a data-toggle="tooltip">Бизнес</a>
							</div>
						</li>
						<li className="nav-item">
							<a href="/members/" className="nav-link">Пространство</a>
						</li>
					</ul>
					<ul className="nav navbar-nav navbar-right">
						<li className="nav-item dropdown">	
							<form action="/search/" method="post" className="form-inline my-2 my-lg-0">
								<input name="search" className="form-control mr-sm-2" type="search" placeholder="Поиск" />
							</form>
						</li>
						<li className="nav-item">
							<a href="/user/"className="nav-link">Логин</a><a href="/sys_sign_out/" className="nav-link">Выйти</a>
							{/* <a href="/login/" className="nav-link">Гость &nbsp; Войти</a> */}
						</li>
					</ul>
				</div>
			</div>
		</nav>
	)
}