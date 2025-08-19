import React, { useState, useEffect, useRef } from 'react';
import { connect } from 'react-redux';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';

import styles from '../../styles/post.module.css';
import { toastAdd } from '../../redux/actions/system';
import { displaySet } from '../../redux/actions/main';
import api from '../../lib/api';
import Grid from '../../components/Post/Grid';
import Feed from '../../components/Post/Feed';
import Paginator from '../../components/Paginator';

const getPage = count => Math.floor(count / 18) + Boolean(count % 18);

export const Posts = ({
  system, main, profile,
  toastAdd, displaySet,
  category = null, page = 1,
  postsLoaded = [], count = null, subcategories = [],
}) => {
  const { t } = useTranslation('common');
  const mounted = useRef(true);
  const router = useRouter();
  const [posts, setPosts] = useState(postsLoaded);
  const [lastPage, setLastPage] = useState(count ? getPage(count) : page);

  // useEffect(() => {
  //   if (main.token && profile.status < 2) {
  //     router.push('/');
  //   }
  // }, [main.token, profile.status]);

  const title = `${category ? category.title : t('structure.posts')} | ${process.env.NEXT_PUBLIC_NAME}`;
  let canonical = process.env.NEXT_PUBLIC_WEB;
  if (category) {
    if (category.locale && category.locale !== process.env.NEXT_PUBLIC_LOCALE) {
      canonical += `${category.locale}/`;
    }
  } else if (router.locale && router.locale !== process.env.NEXT_PUBLIC_LOCALE) {
    canonical += `${router.locale}/`;
  }
  if (category && category.url) {
    canonical += `posts/${category.url}`;
  } else {
    canonical = canonical.slice(0, -1);
  }

  const getPost = (data = {}) => api(main, 'posts.get', data).then(res => {
    if (res.posts) {
      setPosts(res.posts);
      if (res.count) {
        setLastPage(getPage(res.count));
      }
    }
  }).catch(err => toastAdd({
    header: t('system.error'),
    text: err,
    color: 'white',
    background: 'danger',
  }));

  useEffect(() => {
    if (!mounted.current || !posts) {
      getPost({
        category: category && category.id,
        locale: main.locale,
        search: system.search && system.search.length >= 3 ? system.search : '',
        limit: 18,
        offset: (page - 1) * 18,
      });
    }
    mounted.current = false;
  }, [
    system.search && system.search.length >= 3 ? system.search : false,
    main.locale,
    category,
    page,
  ]);

  return (
    <>
      <Head>
        {/* SEO */}
        <title>{ title }</title>
        <meta name="title" content={title} />
        <meta name="og:title" content={title} />
        { category && (
          <>
            { category.description && (
              <>
                <meta name="description" content={category.description} />
                <meta name="og:description" content={category.description} />
              </>
            ) }
            { category.image && (
              <meta name="og:image" content={category.image} />
            ) }
          </>
        ) }
        <meta property="og:url" content={canonical} />
        <meta property="og:type" content="website" />
        <link rel="canonical" href={canonical} />
      </Head>
      <div className={`row ${styles.category}`}>
        <div className="col-md-8">
          { category ? (
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
              { category.parents && category.parents.map((parent, i) => (
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
                key={category.id}
              >
                <meta content={category.parents ? category.parents.length + 1 : 1} itemProp="position" />
                <Link
                  href={`/posts/${category.url}`}
                  title={category.title}
                  itemID={`/posts/${category.url}`}
                  itemScope="itemscope"
                  itemProp="item"
                  itemType="http://schema.org/Thing"
                >
                  <h1 itemProp="name">
                    {category.title}
                  </h1>
                </Link>
              </li>
            </ul>
          ) : (<h1>{ t('structure.posts') }</h1>) }
        </div>
        <div className={`col-md-4 ${styles.tools}`}>
          <div className="btn-group" role="group">
            <button
              type="button"
              className={`btn btn-${main.theme}`}
              onClick={() => displaySet('grid')}
            >
              <i className="fa-solid fa-table-cells-large" />
            </button>
            {/* <button
              type="button"
              className={`btn btn-${main.theme}`}
            >
              <i className="fa-solid fa-list-ul" />
            </button> */}
            <button
              type="button"
              className={`btn btn-${main.theme}`}
              onClick={() => displaySet('feed')}
            >
              <i className="fa-regular fa-image" />
            </button>
          </div>
          { profile.status >= 2 && (
            <Link href="/posts/add" className="btn btn-success ms-3">
              <i className="fa-solid fa-plus" />
            </Link>
          ) }
        </div>
      </div>
      <div className="mb-2">
        { subcategories.map(subcategory => (subcategory.status ? (
          <Link
            href={`/posts/${subcategory.url}/`}
            className={`btn btn-${main.theme} me-2 mb-2`}
            key={subcategory.id}
          >
            { subcategory.title }
          </Link>
        ) : (
          <React.Fragment key={subcategory.id} />
        ))) }
      </div>
      { category && (
        <>
          { category.image && (
            <>
              <img
                src={category.image}
                alt={category.title}
                className={styles.image}
              />
              <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{
                  __html: JSON.stringify({
                    '@context': 'http://schema.org/',
                    '@type': 'ImageObject',
                    contentUrl: category.image,
                    name: category.title,
                    description: category.description,
                  }),
                }}
              />
            </>
          ) }
          <div dangerouslySetInnerHTML={{ __html: category.data }} />
        </>
      ) }
      {
        main.display === 'feed' ? (
          <Feed posts={posts} />
        ) : (
          <Grid posts={posts} />
        )
      }
      <Paginator page={page} lastPage={lastPage} prefix={category ? `/posts/${category.url}` : ''} />
    </>
  );
};

export default connect(state => state, { toastAdd, displaySet })(Posts);

export const getServerSideProps = async ({ query, locale }) => {
  const page = !Number.isNaN(Number(query.page)) ? (+query.page || 1) : 1;
  const res = await api(null, 'posts.get', {
    locale,
    limit: 18,
    offset: (page - 1) * 18,
  }, false, true);
  const subres = await api(null, 'categories.get', { locale }, false, true);

  return {
    props: {
      ...await serverSideTranslations(locale, ['common']),
      page,
      postsLoaded: res.posts || [],
      count: res.count,
      subcategories: subres.categories || [],
    },
  };
};
