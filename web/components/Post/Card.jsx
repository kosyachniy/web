import { useSelector } from 'react-redux';
import Link from 'next/link';

import styles from '../../styles/card.module.css';

export default ({ post }) => {
  const main = useSelector(state => state.main);

  return (
    <Link href={`/posts/${post.url || post.id}`} key={post.id}>
      <div className={`card ${styles.card} ${styles[main.theme]} mb-4 shadow-sm`}>
        { post.image && <div className="card-img-top" style={{ backgroundImage: `url(${post.image})` }} /> }
        <div className="card-body">
          <p className="card-text">
            {/* <span
              className={`badge ${styles.badge} badge-success`}
              style={{ marginRight: '10px', fontSize: '15px' }}
            >
              <img src="/static/icon/{{ icon }}.svg" />
            </span> */}
            { !post.status && <i className="fa-solid fa-lock me-2" /> }
            { post.title }
          </p>

          {/* { post.description && (
          <div className="d-flex justify-content-between align-items-center">
            { post.description }
            <div className="btn-group">
              <button type="button" className="btn btn-sm btn-outline-secondary">View</button>
              <button type="button" className="btn btn-sm btn-outline-secondary">Edit</button>
            </div>
            { post.additionally && <small className="text-muted">{ post.additionally }</small> }
          </div>
          ) } */}
        </div>
      </div>
    </Link>
  );
};
