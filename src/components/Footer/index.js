import React from 'react'

import './style.css'


export default function Header() {
	return (
		<footer class="section footer-classic context-light bg-light">
			<div class="container">
				<div class="row row-30">
					<div class="col-md-4 col-xl-5">
						<div class="pr-xl-4">
							<p><a href="/" class="brand"><img src="/static/logo.svg" alt="Tensegrity" /></a></p>
							<p>Описание</p>
							<p class="rights"><span>©  </span><span class="copyright-year">2018-2019</span><span> </span><span>Название</span><span>. </span><span>Все права защищены</span></p>
						</div>
					</div>
					<div class="col-md-4">
						<h5>Контакты</h5>
						<dl class="contact-list">
							<dt>Адрес</dt>
							<dd>Россия, Санкт-Петербург</dd>
						</dl>
						<dl class="contact-list">
							<dt>Почта</dt>
							<dd><a href="mailto:"></a> <span>&</span> <a href="mailto:"></a></dd>
						</dl>
						<dl class="contact-list">
							<dt>Телефон</dt>
							<dd><a href="tel:"> </a> <span>&</span> <a href="tel:"></a></dd>
						</dl>
					</div>
					<div class="col-md-4 col-xl-3">
						<h5>Ссылки</h5>
						<ul class="nav-list">
							<li><a href="#">О нас</a></li>
							<li><a href="/feedback/?url=">Предложения и ошибки</a></li>
							<li><a href="/codex/">Правила сайта</a></li>
						</ul>
						<a href="/sys_lang/?i=en"><span class="badge"><img src="/static/lang/en.svg" /></span></a>
						<a href="/sys_lang/?i=ru"><span class="badge"><img src="/static/lang/ru.svg" /></span></a>
						<br />
						- соц сети -
					</div>
				</div>
			</div>
		</footer>
	)
}