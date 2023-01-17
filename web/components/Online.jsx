import { useTranslation } from 'next-i18next'
import { useSelector } from 'react-redux'

import styles from '../styles/online.module.css'
import Popup from './Popup'
import Hexagon from './Hexagon'


export default () => {
    const { t } = useTranslation('common')
    const online = useSelector(state => state.online)

    return (
        <div>
            <Popup>
                <h3>{ t('system.online') }</h3>
                { online.users.map(user => (
                    <div className={ styles.user } key={ user.id }>
                        <Hexagon url={ user.image || '/user.png' } />
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
