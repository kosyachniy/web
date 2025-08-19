import { useSelector, useDispatch } from 'react-redux';

import { popupSet } from '../redux/actions/system';
import styles from '../styles/popup.module.css';

export default ({ children }) => {
  const dispatch = useDispatch();
  const main = useSelector(state => state.main);

  return (
    <div className={styles.popup}>
      <div
        className={styles.popup_back}
        onClick={() => dispatch(popupSet(null))}
      />
      <div className={`${styles.popup_cont} bg-${main.theme}`}>
        { children }
      </div>
    </div>
  );
};
