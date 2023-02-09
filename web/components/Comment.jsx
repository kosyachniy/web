import { useTranslation } from 'next-i18next';

import styles from '../styles/comment.module.css';
import Hexagon from './Hexagon';

export const Comment = ({ comment }) => {
  const { t } = useTranslation('common');
  return (
    <div className={styles.comment}>
      <div className={styles.header}>
        <Hexagon url={(comment.user && comment.user.image) || '/user.png'} />
        <div className="ps-2">
          <div className={styles.user}>
            { comment.user ? comment.user.title : t('system.guest') }
          </div>
          <div className={styles.time}>
            вчера
          </div>
        </div>
      </div>
      { comment.data }
    </div>
  );
};

export default ({ comments }) => {
  const { t } = useTranslation('common');
  return (
    <div className={styles.comments}>
      <div className={styles.title}>
        <div>
          <h3>{ t('posts.comments') }</h3>
        </div>
        <div className={styles.counter}>
          { comments.length }
        </div>
      </div>
      <div className="input-group">
        <textarea
          className="form-control"
          placeholder={t('posts.reply')}
        />
        <button
          type="button"
          className="btn btn-success"
        >
          { t('system.send') }
        </button>
      </div>
      { comments && comments.map(
        comment => <Comment comment={comment} key={comment.id} />,
      ) }
    </div>
  );
};
