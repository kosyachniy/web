import React from 'react'

import './style.css'


export default function Header() {
	return (
		<footer className="section footer-classic context-light bg-light">
			<div className="container">
				<div className="row row-30">
					<div className="col-md-4 col-xl-5">
						<div className="pr-xl-4">
							<p><a href="/" className="brand"><img src="/static/logo.svg" alt="Quateo" /></a></p>
							<p>Описание</p>
							<p className="rights"><span>©  </span><span className="copyright-year">2018-2019</span><span> </span><span>Название</span><span>. </span><span>Все права защищены</span></p>
						</div>
					</div>
					<div className="col-md-4">
						<h5>Контакты</h5>
						<dl className="contact-list">
							<dt>Адрес</dt>
							<dd>Россия, Санкт-Петербург</dd>
						</dl>
						<dl className="contact-list">
							<dt>Почта</dt>
							<dd><a href="mailto:"></a> <span>&</span> <a href="mailto:"></a></dd>
						</dl>
						<dl className="contact-list">
							<dt>Телефон</dt>
							<dd><a href="tel:"> </a> <span>&</span> <a href="tel:"></a></dd>
						</dl>
					</div>
					<div className="col-md-4 col-xl-3">
						<h5>Ссылки</h5>
						<ul className="nav-list">
							<li><a href="#">О нас</a></li>
							<li><a href="/feedback/?url=">Предложения и ошибки</a></li>
							<li><a href="/codex/">Правила сайта</a></li>
						</ul>
						<a href="/sys_lang/?i=en"><span className="badge"><img src="/static/lang/en.svg" /></span></a>
						<a href="/sys_lang/?i=ru"><span className="badge"><img src="/static/lang/ru.svg" /></span></a>
						<br />
						- соц сети -
					</div>
				</div>
			</div>
		</footer>
	)
}