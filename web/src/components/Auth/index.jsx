import React from 'react';
import { useTranslation } from 'react-i18next';

// import 'style.css';
import Popup from '../Popup';


const Auth = (props) => {
	const { handlerLogIn } = props;
	const { t } = useTranslation();

	return (
		<div id="auth">
			<Popup handlerLogIn={handlerLogIn} >
				<a
					href={``}
					className="btn btn_vk"
				>
					<img src="/social/vk.png" alt="VK" />
				</a>
				<a
					href={``}
					className="btn btn_google"
				>
					<img src="/social/google.png" alt="Google" />
				</a>
				<div className="btn btn_green">
					<i className="fas fa-phone" />
				</div>
				<div className="btn btn_green">
					<i className="fas fa-envelope" />
				</div>
			</Popup>
		</div>
	);
};

export default Auth;