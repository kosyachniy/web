import React from 'react'

import './style.css'
import { name, description, address, mail, phone, social } from '../../sets'


export default function Header() {
	return (
		<footer className="section footer-classic context-light bg-light">
			<div className="container">
				<div className="row row-30">
					<div className="col-md-4 col-xl-5">
						<div className="pr-xl-4">
							<p><a href="/" className="brand"><img src="/brand/logo.svg" alt={ name } /></a></p>
							<p>{ description }</p>
							<p className="rights"><span>©  </span><span className="copyright-year">2018-2019</span><span> </span><span>{ name }</span><span>. </span><span>Все права защищены</span></p>
						</div>
					</div>
					<div className="col-md-4">
						<h5>Контакты</h5>
						<dl className="contact-list">
							<dt>Адрес</dt>
							<dd>{ address }</dd>
						</dl>
						<dl className="contact-list">
							<dt>Почта</dt>
							<dd><a href={ 'mailto:' + mail }>{ mail }</a></dd>
						</dl>
						<dl className="contact-list">
							<dt>Телефон</dt>
							<dd><a href={ 'tel:' + phone}>{ phone }</a></dd>
						</dl>
					</div>
					<div className="col-md-4 col-xl-3">
						<h5>Ссылки</h5>
						<ul className="nav-list">
							<li><a href="#">О нас</a></li>
							<li><a href="/feedback/?url=">Предложения и ошибки</a></li>
							<li><a href="/codex/">Правила сайта</a></li>
						</ul>
						<span className="badge"><img src="/lang/en.svg" /></span>
						<span className="badge"><img src="/lang/ru.svg" /></span>
						<br />
						{ social.map((el, num) =>
							<a href={ el.cont } key={ num }><span className="badge"><img src={ '/social/' + el.name + '.ico' } /></span></a>
						) }
					</div>
				</div>
			</div>
		</footer>
	)
}