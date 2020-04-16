import React from 'react';

import './style.css';
import Popup from '../../../components/Popup';


const Auth = (props) => {
	const { handlerPopUp } = props;

	return (
		<div id="auth">
			<Popup handlerPopUp={handlerPopUp} >
				<a
					href={`/#vk`}
					className="btn btn_vk"
				>
					<img src="/social/vk.png" alt="VK" />
				</a>
				<a
					href={`/#google`}
					className="btn btn_google"
				>
					<img src="/social/google.png" alt="Google" />
				</a>
				<div className="btn btn_green">
					<i className="fas fa-phone" />
				</div>
				<div
					className="btn btn_green"
					onClick={ ()=>{handlerPopUp('mail')} }
				>
					<i className="fas fa-envelope" />
				</div>
			</Popup>
		</div>
	);
};

export default Auth;