import React from 'react'
import { useTranslation } from 'react-i18next';

import './style.css';
import Popup from '../../../components/Popup';
import Hexagon from '../../../components/Hexagon';


const Online = (props) => {
    const { system, online, handlerPopUp } = props
    const { t } = useTranslation()

    return (
        <div id="online">
            <Popup handlerPopUp={handlerPopUp} theme={system.theme} >
                <h3>{t('system.online')}</h3>
                { online.users.map(user => (
                    <div className="user" key={ user.id }>
                        <Hexagon url={ user.avatar || '/user.png' } />
                        <div>
                            {
                                user.name && user.surname ? (
                                    `${user.name || ''} ${user.surname || ''} (@${user.login})`
                                ) : (
                                    `@${user.login}`
                                )
                            }
                        </div>
                    </div>
                )) }
            </Popup>
        </div>
    );
};

export default Online;
