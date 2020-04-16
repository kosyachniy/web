import React, {useState} from 'react';
import { useTranslation } from 'react-i18next';

import api from '../../../func/api'

// import './style.css';


const checkPassword = password => {
	return (password.search(/\d/) !== -1) && (password.search(/[A-Za-z]/) !== -1);
}

const Profile = (props) => {
	const { profile, profileUpdate } = props
	const { t } = useTranslation()

	const [state, setState] = useState({
		login: profile.login,
		name: profile.name,
		surname: profile.surname,
		mail: profile.mail,
		password: '',
	})

	const accountEdit = () => {
		const handlerSuccess = res => {
			profileUpdate({
				login: state.login,
				name: state.name,
				surname: state.surname,
				mail: state.mail,
				password: state.password,
				// avatar: res.avatar,
			})
		}

		const data = {
			login: state.login,
			name: state.name,
			surname: state.surname,
			mail: state.mail,
		}

		if (state.password.length) {
			data['password'] = state.password
		}

		api('account.edit', data, handlerSuccess)
	}

	return (
		<div className="album py-5">
			<div className="container">
				<form>
					<div class="input-group  mb-3">
						<input
							value={state.name}
							onChange={(event) => { setState({ ...state, name: event.target.value }) }}
							placeholder={t('profile.name')}
							type="text"
							aria-label="First name"
							className="form-control"
						/>
						<input
							value={state.surname}
							onChange={(event) => { setState({ ...state, surname: event.target.value }) }}
							placeholder={t('profile.surname')}
							type="text"
							aria-label="Last name"
							className="form-control"
						/>
					</div>
					<div className="input-group flex-nowrap mb-3">
						<div className="input-group-prepend">
							<span className="input-group-text" id="addon-wrapping">@</span>
						</div>
						<input
							value={state.login}
							onChange={(event) => { setState({ ...state, login: event.target.value }) }}
							placeholder={t('profile.login')}
							type="text"
							className="form-control"
							aria-label="Username"
							aria-describedby="addon-wrapping"
						/>
					</div>
					<div className="input-group mb-3">
						<input
							value={state.mail}
							onChange={(event) => { setState({ ...state, mail: event.target.value }) }}
							placeholder={t('profile.mail')}
							type="email"
							className="form-control"
							autocomplete="false"
						/>
					</div>
					<div class="form-group">
						<input
							value={state.password}
							onChange={(event) => { setState({ ...state, password: event.target.value }) }}
							placeholder={t('profile.password')}
							type="password"
							class="form-control"
							autocomplete="false"
						/>
					</div>
					<input
						type="button"
						class="btn btn-success"
						value={t('system.save')}
						onClick={accountEdit}
					/>
				</form>
			</div>
		</div>
	);
};

export default Profile;