import { useTranslation } from 'next-i18next';
import { useSelector, useDispatch } from 'react-redux';

import styles from '../styles/online.module.css';
import { popupSet } from '../redux/actions/system';
import Popup from './Popup';
import Hexagon from './Hexagon';

export const Online = () => {
  const { t } = useTranslation('common');
  const dispatch = useDispatch();
  const online = useSelector(state => state.online);

  return (
    <div className={styles.line}>
      { online.count ? (
        <>
          { t('system.online') }
          <div className={styles.online} />
          <div
            className="badge bg-secondary pe-2"
            onClick={() => dispatch(popupSet('online'))}
          >
            { online.count }
          </div>
        </>
      ) : (
        <>
          { t('system.offline') }
          <div className={styles.offline} />
        </>
      )}
    </div>
  );
};

export default () => {
  const { t } = useTranslation('common');
  const online = useSelector(state => state.online);

  return (
    <div>
      <Popup>
        <h2>{ t('system.online') }</h2>
        { online.users.map(user => (
          <div className={styles.user} key={user.id}>
            <Hexagon url={user.image || '/user.png'} />
            <div>
              { user.name && user.surname ? (
                `${user.name || ''} ${user.surname || ''} (@${user.login})`
              ) : (
                `@${user.login}`
              ) }
            </div>
          </div>
        )) }
      </Popup>
    </div>
  );
};
