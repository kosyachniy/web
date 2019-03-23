import React from 'react'

import './style.css'


export default function Header() {
	return (
		<nav class="navbar navbar-expand-lg navbar-light bg-light sticky-top">
			<div class="container">
				<a href="/" class="navbar-brand"><img src="/static/logo_dark.svg" /></a>
				<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				</button>

				<div class="collapse navbar-collapse" id="navbarTogglerDemo02">
					<ul class="navbar-nav mr-auto mt-2 mt-lg-0">
						<li class="nav-item dropdown">
							<a href="/learn/" class="nav-link">Ла</a>
							{/* <a href="/admin/add/ladder/"><span class="badge badge-dark">+</span></a> */}
							<div class="dropdown-content">
								<a href="/learn/ladders/" data-toggle="tooltip">Лу</a>
								<a data-toggle="tooltip">Ле</a>
							</div>
						</li>
						<li class="nav-item">
							<a href="/members/" class="nav-link">Ва</a>
						</li>
					</ul>
					<ul class="nav navbar-nav navbar-right">
						<li class="nav-item dropdown">	
							<form action="/search/" method="post" class="form-inline my-2 my-lg-0">
								<input name="search" class="form-control mr-sm-2" type="search" placeholder="Поиск" />
							</form>
						</li>
						<li class="nav-item">
							<a href="/user/"class="nav-link">Логин</a><a href="/sys_sign_out/" class="nav-link">Выйти</a>
							{/* <a href="/login/" class="nav-link">Гость &nbsp; Войти</a> */}
						</li>
					</ul>
				</div>
			</div>
		</nav>
	)
}