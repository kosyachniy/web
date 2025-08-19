import { useSelector } from 'react-redux';
import Link from 'next/link';
import { useTranslation } from 'next-i18next';

import styles from '../../styles/feed.module.css';

export default ({ posts }) => {
  const { t } = useTranslation('common');
  const profile = useSelector(state => state.profile);

  const getTime = time => {
    const newTime = new Date(time * 1000);

    const year = newTime.getFullYear();
    let day = `${newTime.getDate()}`;
    let hours = `${newTime.getHours()}`;
    let minutes = `${newTime.getUTCMinutes()}`;
    const month = [
      t('months.january'), t('months.february'), t('months.march'),
      t('months.april'), t('months.may'), t('months.june'),
      t('months.july'), t('months.august'), t('months.september'),
      t('months.october'), t('months.november'), t('months.december'),
    ][newTime.getMonth()];

    if (day.length < 2) {
      day = `0${day}`;
    }

    if (hours.length < 2) {
      hours = `0${hours}`;
    }

    if (minutes.length < 2) {
      minutes = `0${minutes}`;
    }

    return `${day} ${month} ${year} в ${hours}:${minutes}`;
  };

  return (
    <div className={`container ${styles.feed}`}>
      { profile.status >= 2 && (
        <Link
          href="/posts/add"
          className="btn btn-success"
          style={{ width: '100%' }}
        >
          <i className="fa-solid fa-plus" />
        </Link>
      ) }

      { !posts.length && (
      <p>
        { t('posts.empty') }
        !
      </p>
      ) }

      { posts.map(post => (
        <div className={styles.cards} key={post.id}>
          <Link href={`/posts/${post.id}`}>
            <>
              <div className="cards-content">
                <h3 className={styles.title}>{ post.title }</h3>
                <div className={styles.additional}><i className="bi bi-three-dots-vertical" /></div>
                <div className={styles.time}>{ getTime(post.created) }</div>
              </div>
              { post.image && (
              <img src={post.image} alt={post.title} />
              ) }
              <div className="cards-content">
                <div className={`${styles.content} ${styles.short}`}>{ post.data }</div>
              </div>
            </>
          </Link>
          <div className={`cards-content ${styles.reactions}`}>
            <div>
              <i className="fa-regular fa-heart" />
              { post.reactions ? ` ${post.reactions}` : '' }
            </div>
            {/* <i className="fa-solid fa-heart" /> */}
            <div>
              <i className="fa-regular fa-comment" />
              {' '}
              { post.comments && post.comments.length ? ` ${post.comments.length}` : '' }
            </div>
            <div>
              <i className="fa-solid fa-share" />
              { post.reposts ? ` ${post.reposts}` : '' }
            </div>
          </div>
        </div>
      )) }
    </div>
  );
};
