import React from 'react';

import './style.css';


const Popup = (props) => {
	const { children, handlerLogIn } = props;

	return (
		<div className="popup">
			<div className="popup_back" onClick={ ()=>{handlerLogIn(false)} } />
			<div className="popup_cont">
				{children}
			</div>
		</div>
	);
};

export default Popup;