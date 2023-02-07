import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { useTranslation } from 'next-i18next';
// import MathJax from 'react-mathjax-preview'

import styles from '../../styles/post.module.css';
import { toastAdd } from '../../redux/actions/system';
import { categoriesClear } from '../../redux/actions/categories';
import api from '../../lib/api';
import Upload from '../Forms/Upload';
import Locale from '../Forms/Locale';
import Category from '../Forms/Category';
import Editor from '../Forms/Editor';

export const Edit = ({ post, setEdit, setPost }) => {
  const { t } = useTranslation('common');
  const dispatch = useDispatch();
  const router = useRouter();
  const main = useSelector(state => state.main);
  const [title, setTitle] = useState(post ? post.title : '');
  const [data, setData] = useState(post ? post.data : '');
  const [image, setImage] = useState(post ? post.image : null);
  const [locale, setLocale] = useState(post ? post.locale : main.locale);
  const [category, setCategory] = useState(post ? post.category : null);
  const [editorLoaded, setEditorLoaded] = useState(false);

  const editPost = () => {
    const req = {
      title, data, image, locale, category,
    };

    if (post) {
      req.id = post.id;
    }

    api(main, 'posts.save', req).then(res => {
      if (post) {
        setPost(null);
        setEdit(false);
      } else {
        router.push(`/posts/${res.id}`);
      }
      dispatch(toastAdd({
        header: t('system.success'),
        text: t('system.saved'),
        color: 'white',
        background: 'success',
      }));
    }).catch(err => {
      if (post) {
        setEdit(false);
      }
      dispatch(toastAdd({
        header: t('system.error'),
        text: err,
        color: 'white',
        background: 'danger',
      }));
    });
  };

  useEffect(() => {
    setEditorLoaded(true);
  }, []);

  return (
    <div>
      <div className="album py-5">
        <div className="input-group mb-3">
          <input
            type="text"
            className={`form-control ${styles.title}`}
            placeholder={t('posts.title')}
            value={title}
            onChange={event => setTitle(event.target.value)}
          />
        </div>
        <div className="row py-3">
          <div className="col-12 col-md-6 pb-3">
            <Upload image={image} setImage={setImage} />
          </div>
          <div className="col-12 col-md-6">
            <Locale locale={locale} setLocale={setLocale} />
            <Category
              category={category}
              setCategory={setCategory}
            />
          </div>
        </div>

        <Editor
          editorLoaded={editorLoaded}
          data={data}
          updatePost={text => setData(text)}
        />
        <br />
        <button
          type="button"
          className="btn btn-success"
          style={{ width: '100%' }}
          onClick={editPost}
        >
          <i className="fa-regular fa-floppy-disk" />
        </button>
      </div>
    </div>
  );
};

export default ({ post, setPost }) => {
  const { t } = useTranslation('common');
  const dispatch = useDispatch();
  const router = useRouter();
  const main = useSelector(state => state.main);
  const profile = useSelector(state => state.profile);
  const [edit, setEdit] = useState(false);
  const [toasts, setToasts] = useState([]);

  const rmPost = () => api(main, 'posts.rm', { id: post.id }).then(() => {
    router.push('/');
    dispatch(toastAdd({
      header: t('system.success'),
      text: t('system.deleted'),
      color: 'white',
      background: 'success',
    }));
  }).catch(() => dispatch(toastAdd({
    header: t('system.error'),
    text: t('system.no_access'),
    color: 'white',
    background: 'danger',
  })));

  const blockPost = ({ status }) => api(main, 'posts.save', { id: post.id, status }).then(() => {
    setPost(null);
    setEdit(null);
    dispatch(categoriesClear());
    dispatch(toastAdd({
      header: t('system.success'),
      text: status ? t('system.unblocked') : t('system.blocked'),
      color: 'white',
      background: 'success',
    }));
  }).catch(err => dispatch(toastAdd({
    header: t('system.error'),
    text: err,
    color: 'white',
    background: 'danger',
  })));

  if (!post) {
    return (
      <></>
    );
  }

  return (
    <div className={`album py-2 ${styles.post}`}>
      <div className="row">
        <div className="col-md-8">
          <h1>{ post.title }</h1>
        </div>
        <div className="col-md-4 mb-3" style={{ textAlign: 'right' }}>
          { profile.status >= 2 && (
            <>
              <button
                type="button"
                className="btn btn-outline-secondary"
                onClick={() => setEdit(!edit)}
              >
                <i className={edit ? 'fa-regular fa-eye' : 'fa-solid fa-pencil'} />
              </button>
              { post.status ? (
                <button
                  type="button"
                  className="btn btn-danger"
                  onClick={() => blockPost({ status: 0 })}
                >
                  <i className="fa-solid fa-lock" />
                </button>
              ) : (
                <button
                  type="button"
                  className="btn btn-success"
                  onClick={() => blockPost({ status: 1 })}
                >
                  <i className="fa-solid fa-lock-open" />
                </button>
              ) }
              <button
                type="button"
                className="btn btn-danger"
                onClick={rmPost}
              >
                <i className="fa-solid fa-trash" />
              </button>
            </>
          ) }
        </div>
      </div>

      { post.category_data && (
        <>
          { post.category_data.parents && post.category_data.parents.map(parent => (
            <React.Fragment key={parent.id}>
              <Link
                href={`/posts/${parent.url}`}
                style={{ textDecoration: 'underline dotted' }}
              >
                {parent.title}
              </Link>
              {' / '}
            </React.Fragment>
          )) }
          <Link
            href={`/posts/${post.category_data.url}`}
            style={{ textDecoration: 'underline dotted' }}
          >
            {post.category_data.title}
          </Link>
          <br />
          <br />
        </>
      ) }

      { edit ? (
        <Edit
          post={post}
          setEdit={setEdit}
          setPost={setPost}
          toasts={toasts}
          setToasts={setToasts}
        />
      ) : (
        <>
          { post.image && <img src={post.image} alt={post.title} className={styles.image} /> }

          <div dangerouslySetInnerHTML={{ __html: post.data }} />

          {/* <MathJax
            math={post.data}
            sanitizeOptions={{
              USE_PROFILES: {
                html: true,
                mathMl: true,
              },
            }}
          /> */}

          {/* <div style={{ marginTop: '50px', height: '250px' }}>
            { post.geo ? (
              <Map center={post.geo} zoom={14} />
            ) : (
              <Map />
            )}
          </div> */}
        </>
      ) }
    </div>
  );
};
