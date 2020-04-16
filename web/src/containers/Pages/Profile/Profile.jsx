import React, {useState} from 'react';
import { Redirect } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import api from '../../../func/api'
import Avatar from '../../../components/Avatar'


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
		avatar: profile.avatar,
		file: null,
	})

	const accountEdit = () => {
		const handlerSuccess = res => {
			profileUpdate({
				login: state.login,
				name: state.name,
				surname: state.surname,
				mail: state.mail,
				password: state.password,
				avatar: res.avatar,
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

		if (state.avatar !== profile.avatar) {
			data['avatar'] = state.avatar
			data['file'] = state.file
		}

		api('account.edit', data, handlerSuccess)
	}

	const updateAvatar = (avatar, file) => {
		setState({ ...state, avatar, file })
	}

	if (profile.id === 0) {
		return (<Redirect to="/" />)
	}

	return (
		<div className="album py-5">
			<div className="container">
				<Avatar avatar={state.avatar} file={state.file} updateAvatar={updateAvatar} />
				<form>
					<div className="input-group mb-3">
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
							autoComplete="false"
						/>
					</div>
					<div className="form-group">
						<input
							value={state.password}
							onChange={(event) => { setState({ ...state, password: event.target.value }) }}
							placeholder={t('profile.password')}
							type="password"
							className="form-control"
							autoComplete="false"
						/>
					</div>
					<input
						type="button"
						className="btn btn-success"
						value={t('system.save')}
						onClick={accountEdit}
					/>
				</form>
			</div>
		</div>
	);
};

export default Profile;