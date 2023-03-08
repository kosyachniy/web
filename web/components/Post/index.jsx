import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import { useTranslation } from 'next-i18next';
// import MathJax from 'react-mathjax-preview'

import styles from '../../styles/post.module.css';
import { toastAdd } from '../../redux/actions/system';
import { categoriesClear } from '../../redux/actions/categories';
import api from '../../lib/api';
import { getISO, getTime } from '../../lib/format';
import Upload from '../Forms/Upload';
import Locale from '../Forms/Locale';
import Category from '../Forms/Category';
import Editor from '../Forms/Editor';
import Comments from '../Comment';
import Hexagon from '../Hexagon';
import Card from './Card';

export const Edit = ({ post, setEdit, setPost }) => {
  const { t } = useTranslation('common');
  const dispatch = useDispatch();
  const router = useRouter();
  const main = useSelector(state => state.main);
  const [title, setTitle] = useState(post ? post.title : '');
  const [description, setDescription] = useState(post ? post.description : '');
  const [data, setData] = useState(post ? post.data : '');
  const [image, setImage] = useState(post ? post.image : null);
  const [locale, setLocale] = useState(post ? post.locale : main.locale);
  const [category, setCategory] = useState(post ? post.category : null);
  const [editorLoaded, setEditorLoaded] = useState(false);

  const editPost = () => {
    const req = {
      title, description, data, image, locale, category,
    };

    if (post) {
      req.id = post.id;
    }

    api(main, 'posts.save', req).then(res => {
      if (post) {
        setPost(null);
        setEdit(false);
      } else {
        router.push(`/posts/${res.post.url}`);
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
            <textarea
              className="form-control"
              placeholder={`${t('posts.description')} (SEO)`}
              value={description}
              onChange={event => setDescription(event.target.value)}
              style={{ height: '146px' }}
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
  const [created, setCreated] = useState(null);
  const [posts, setPosts] = useState([]);

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

  useEffect(() => {
    if (main.token && post) {
      // Formatted time
      setCreated(getTime(post.created));

      // Recommendations
      api(main, 'posts.guess', {
        id: post.id,
        category: post.category,
        locale: router.locale,
      }).then(res => {
        if (res.posts) {
          setPosts(res.posts);
        }
      });
    }
  }, [main.token, post && post.id]);

  if (!post) {
    return (
      <></>
    );
  }

  let canonical = process.env.NEXT_PUBLIC_WEB;
  if (post.locale && post.locale !== process.env.NEXT_PUBLIC_LOCALE) {
    canonical += `${post.locale}/`;
  }
  canonical += `posts/${post.url}`;

  return (
    <div className={`album pb-2 ${styles.post}`}>
      <Head>
        {/* SEO */}
        <title>{ `${post.title} | ${process.env.NEXT_PUBLIC_NAME}` }</title>
        <meta name="title" content={`${post.title} | ${process.env.NEXT_PUBLIC_NAME}`} />
        <meta name="og:title" content={`${post.title} | ${process.env.NEXT_PUBLIC_NAME}`} />
        <meta name="description" content={post.description} />
        <meta name="og:description" content={post.description} />
        { post.image && (
          <meta name="og:image" content={post.image} />
        ) }
        <meta property="og:url" content={`${process.env.NEXT_PUBLIC_WEB}posts/${post.url}`} />
        <meta property="og:type" content="article" />
        <link rel="canonical" href={canonical} />
      </Head>
      <div className="row">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'http://schema.org/',
              '@type': 'Article',
              mainEntityOfPage: {
                '@type': 'WebPage',
                '@id': `${process.env.NEXT_PUBLIC_WEB}posts/${post.url}`,
              },
              headline: post.title,
              image: post.image || '',
              datePublished: getISO(post.created),
              dateModified: getISO(post.updated),
              text: post.description,
              author: [{
                '@type': 'Person',
                name: post.author ? `${post.author.title} ${post.author.id}` : '',
              }],
              publisher: {
                '@type': 'Organization',
                name: process.env.NEXT_PUBLIC_NAME,
                logo: {
                  '@type': 'ImageObject',
                  url: `${process.env.NEXT_PUBLIC_WEB}brand/logo.png`,
                },
              },
              url: `${process.env.NEXT_PUBLIC_WEB}posts/${post.url}`,
            }),
          }}
        />
        <div className="col-md-8">
          <h1>{ post.title }</h1>
          <div className={styles.info}>
            { post.category_data && (
              <ul
                role="navigation"
                aria-label="breadcrumb"
                itemScope="itemscope"
                itemType="http://schema.org/BreadcrumbList"
                className={styles.navigation}
              >
                <li
                  itemProp="itemListElement"
                  itemScope="itemscope"
                  itemType="http://schema.org/ListItem"
                >
                  <meta content="0" itemProp="position" />
                  <Link
                    href="/posts"
                    style={{ textDecoration: 'underline dotted' }}
                    title={t('system.main')}
                    itemID="/posts"
                    itemScope="itemscope"
                    itemProp="item"
                    itemType="http://schema.org/Thing"
                  >
                    <span itemProp="name">{ t('system.main') }</span>
                  </Link>
                  <span>&nbsp;/&nbsp;</span>
                </li>
                { post.category_data.parents && post.category_data.parents.map((parent, i) => (
                  <li
                    itemProp="itemListElement"
                    itemScope="itemscope"
                    itemType="http://schema.org/ListItem"
                    key={parent.id}
                  >
                    <meta content={i + 1} itemProp="position" />
                    <Link
                      href={`/posts/${parent.url}`}
                      style={{ textDecoration: 'underline dotted' }}
                      title={parent.title}
                      itemID={`/posts/${parent.url}`}
                      itemScope="itemscope"
                      itemProp="item"
                      itemType="http://schema.org/Thing"
                    >
                      <span itemProp="name">
                        {parent.title}
                      </span>
                    </Link>
                    <span>&nbsp;/&nbsp;</span>
                  </li>
                )) }
                <li
                  itemProp="itemListElement"
                  itemScope="itemscope"
                  itemType="http://schema.org/ListItem"
                  key={post.category_data.id}
                >
                  <meta content={post.category_data.parents ? post.category_data.parents.length + 1 : 1} itemProp="position" />
                  <Link
                    href={`/posts/${post.category_data.url}`}
                    style={{ textDecoration: 'underline dotted' }}
                    title={post.category_data.title}
                    itemID={`/posts/${post.category_data.url}`}
                    itemScope="itemscope"
                    itemProp="item"
                    itemType="http://schema.org/Thing"
                  >
                    <span itemProp="name">
                      {post.category_data.title}
                    </span>
                  </Link>
                </li>
              </ul>
            ) }
          </div>
        </div>
        <div className={`col-md-4 ${styles.tools}`}>
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
          <div className="row">
            <div className="col-md-8">
              { post.image && (
                <>
                  <img src={post.image} alt={post.title} className={styles.image} />
                  <script
                    type="application/ld+json"
                    dangerouslySetInnerHTML={{
                      __html: JSON.stringify({
                        '@context': 'http://schema.org/',
                        '@type': 'ImageObject',
                        contentUrl: post.image,
                        name: post.title,
                        description: post.description,
                      }),
                    }}
                  />
                </>
              ) }

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
            </div>
            <div className={`col-md-4 ${styles.side}`}>
              <div className={styles.about}>
                { post.author && post.author.title ? (
                  <div className={styles.user}>
                    <div className="me-2">
                      <Hexagon url={post.author.image || '/user.png'} />
                    </div>
                    {post.author.title ? post.author.title : t('system.guest')}
                  </div>
                ) : (<></>) }
                <div>
                  <i className="fa-solid fa-pencil me-2" />
                  { created }
                </div>
                { post.views ? (
                  <div>
                    <i className="fa-regular fa-eye me-2" />
                    { post.views }
                  </div>
                ) : (<></>) }
              </div>
              <div>
                <div className={styles.header}>
                  <i className="bi bi-fire me-2" />
                  {t('system.popular')}
                </div>
                { posts.map(post => <Card post={post} key={post.id} />) }
              </div>
            </div>
          </div>

          <Comments post={post.id} comments={post.comments} />
        </>
      ) }
    </div>
  );
};
