import React from 'react';
import { useTranslation } from 'react-i18next';

import './style.css';
import Popup from '../../../components/Popup';
import Hexagon from '../../../components/Hexagon';


const Online = (props) => {
	const { online, handlerPopUp } = props
	const { t } = useTranslation()

	return (
		<div id="online">
			<Popup handlerPopUp={handlerPopUp} >
				<h3>{t('system.online')}</h3>
				{ online.users.map(user => (
					<div className="user" key={ user.id }>
						<Hexagon url={ user.avatar } />
						<div>
							{ `${user.name} ${user.surname} (@${user.login})` }
						</div>
					</div>
				)) }
			</Popup>
		</div>
	);
};

export default Online;