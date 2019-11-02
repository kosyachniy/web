import React from 'react'
import { Link } from 'react-router-dom'

import './style.css'
import { name, description, address, mail, phone, social } from '../../../sets'


export default function Footer(props) {
	return (
		<footer className="section footer-classic context-light bg-light">
			<div className="container">
				<div className="row row-30">
					<div className="col-md-4 col-xl-5">
						<div className="pr-xl-4">
							<p><Link to="/" className="brand"><img src="/brand/logo.svg" alt={ name } /></Link></p>
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
							<dd><a href={ 'tel:' + phone }>{ phone }</a></dd>
						</dl>
					</div>
					<div className="col-md-4 col-xl-3">
						<h5>Ссылки</h5>
						<ul className="nav-list">
							<li><Link to="/about/">О нас</Link></li>
							<li><Link to="/feedback/">Предложения и ошибки</Link></li>
							<li><Link to="/codex/">Правила сайта</Link></li>
						</ul>
						<span className="badge" onClick={ () => {props.handlerLang('en')} }><img src="/lang/en.svg" /></span>
						<span className="badge" onClick={ () => {props.handlerLang('ru')} }><img src="/lang/ru.svg" /></span>
						<br />
						<div className="social">
							{ social.map((el, num) =>
								<a href={ el.cont } key={ num }><span className="badge"><img src={ '/social/' + el.name + '.ico' } /></span></a>
							) }
						</div>
					</div>
				</div>
			</div>
		</footer>
	)
}