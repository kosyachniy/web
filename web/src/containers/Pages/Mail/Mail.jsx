import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'

import api from '../../../func/api'

import './style.css'
import Popup from '../../../components/Popup'


const checkPassword = password => {
	return (password.search(/\d/) !== -1) && (password.search(/[A-Za-z]/) !== -1)
}

const Auth = (props) => {
	const [state, setState] = useState({
		mail: '',
		password: '',
	})

	const { profileIn, handlerPopUp } = props
	const { t } = useTranslation()

	const signIn = () => {
		const handlerSuccess = res => {
			profileIn(res)
			handlerPopUp(false)
		}

		const handlerError = res => {
			console.log(res)
		}

		const data = {login: state.mail, password: state.password}
		api('account.auth', data, handlerSuccess, handlerError)
	}

	return (
		<div id="mail">
			<Popup handlerPopUp={handlerPopUp} >
				<div className="form-group">
					<input
						className="form-control"
						type="text"
						placeholder={t('profile.mail')}
						value={state.mail}
						onChange={(event) => { setState({ ...state, mail: event.target.value }) }}
						autoComplete="off"
						required
					/>
				</div>
				<div className="form-group">
					<input
						className="form-control"
						// className={(responce !== null && responce.result === 'password') ? 'error' : ''}
						type="password"
						placeholder={t('profile.password')}
						value={state.password}
						onChange={(event) => { setState({ ...state, password: event.target.value }) }}
						autoComplete="off"
						required
					/>
				</div>
				<div className="pass_info">
					<span style={state.password.length >= 6 ? {} : { color: '#e74c3c' }}>
						<i className="fas fa-genderless" />
						{ t('profile.passwordTip1') }
					</span>
					<span style={checkPassword(state.password) ? {} : { color: '#e74c3c' }}>
						<i className="fas fa-genderless" />
						{ t('profile.passwordTip2') }
					</span>
				</div>
				<input
					type="button"
					className="btn btn-success"
					value={t('system.sign_in')}
					onClick={signIn}
				/>
			</Popup>
		</div>
	);
};

export default Auth;