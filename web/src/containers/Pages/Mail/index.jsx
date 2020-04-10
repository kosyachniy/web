import React, {useState} from 'react';
import { useTranslation } from 'react-i18next';

import './style.css';
import Popup from '../../../components/Popup';


function checkPassword(password) {
	let res = false;

    if ((password.search(/\d/) !== -1) && (password.search(/[A-Za-z]/) !== -1)) {
        res = true;
	}

    return res;
}

const Auth = (props) => {
	const [state, setState] = useState({
		mail: '',
		password: '',
	});

	const { handlerPopUp } = props;
	const { t } = useTranslation();

	const signIn = () => {
		console.log(`${state.mail} — ${state.password}`)
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
					type="submit"
					className="btn btn-success"
					value={t('system.sign_in')}
					onClick={signIn}
				/>
			</Popup>
		</div>
	);
};

export default Auth;