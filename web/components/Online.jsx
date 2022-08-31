import { useTranslation } from 'next-i18next'

import styles from '../../../styles/online.module.css'
import Popup from './Popup';
import Hexagon from './Hexagon';


export default ({ system, online, handlerPopUp }) => {
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
    )
}
