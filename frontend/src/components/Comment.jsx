import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useTranslation } from 'next-i18next';

import styles from '../styles/comment.module.css';
import { toastAdd } from '../redux/actions/system';
import api from '../lib/api';
import { getTime } from '../lib/format';
import Hexagon from './Hexagon';

export const Comment = ({ comment }) => {
  const { t } = useTranslation('common');
  const [time, setTime] = useState(null);

  useEffect(() => {
    setTime(getTime(comment.created));
  }, []);

  return (
    <div className={styles.comment}>
      <div className={styles.header}>
        <Hexagon url={(comment.user && comment.user.image) || '/user.png'} />
        <div className="ps-2">
          <div className={styles.user}>
            { comment.user && comment.user.title ? comment.user.title : t('system.guest') }
          </div>
          <div className={styles.time}>
            { time }
          </div>
        </div>
      </div>
      { comment.data }
    </div>
  );
};

export default ({ post, comments }) => {
  const { t } = useTranslation('common');
  const dispatch = useDispatch();
  const main = useSelector(state => state.main);
  const profile = useSelector(state => state.profile);
  const [replies, setReplies] = useState(comments || []);
  const [data, setData] = useState(post ? post.data : '');

  const saveComment = () => {
    if (!data) {
      return;
    }
    api(main, 'posts.reply', { post, data }).then(res => {
      setData('');
      setReplies([{ ...res.comment, user: profile }, ...replies]);
    }).catch(err => {
      dispatch(toastAdd({
        header: t('system.error'),
        text: err,
        color: 'white',
        background: 'danger',
      }));
    });
  };

  return (
    <div className={styles.comments}>
      <div className={styles.title}>
        <div>
          <h2>{ t('posts.comments') }</h2>
        </div>
        <div className={styles.counter}>
          <h2>
            { replies.length }
          </h2>
        </div>
      </div>
      <div className="input-group">
        <textarea
          className="form-control"
          placeholder={t('posts.reply')}
          value={data}
          onChange={event => setData(event.target.value)}
        />
        <button
          type="button"
          className="btn btn-success"
          onClick={saveComment}
        >
          { t('system.send') }
        </button>
      </div>
      { replies && replies.map(
        comment => <Comment comment={comment} key={comment.id} />,
      ) }
    </div>
  );
};
