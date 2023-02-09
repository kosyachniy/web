import React, { useState, useEffect, useRef } from 'react';
import { connect } from 'react-redux';
import Link from 'next/link';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';

import styles from '../../styles/post.module.css';
import { toastAdd } from '../../redux/actions/system';
import { displaySet } from '../../redux/actions/main';
import api from '../../lib/api';
import { getFirst } from '../../lib/format'
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
  const [posts, setPosts] = useState(postsLoaded);
  const [lastPage, setLastPage] = useState(count ? getPage(count) : page);

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
      <div className={`row ${styles.category}`}>
        <div className="col-8">
          { category ? (
            <ul
              role="navigation"
              aria-label="breadcrumb"
              itemScope="itemscope"
              itemType="http://schema.org/BreadcrumbList"
              className={styles.navigation}
            >
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
                    itemid={`/posts/${parent.url}`}
                    itemscope="itemscope"
                    itemprop="item"
                    itemtype="http://schema.org/Thing"
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
                  itemid={`/posts/${category.url}`}
                  itemscope="itemscope"
                  itemprop="item"
                  itemtype="http://schema.org/Thing"
                >
                  <h1 itemProp="name">
                    {category.title}
                  </h1>
                </Link>
              </li>
            </ul>
          ) : (<h1>{ t('structure.posts') }</h1>) }
        </div>
        <div className="col-4" style={{ textAlign: 'right' }}>
          <div className="btn-group mb-2" role="group">
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
            <Link href="/posts/add">
              <button
                type="button"
                className="btn btn-success ms-3 mb-2"
              >
                <i className="fa-solid fa-plus" />
              </button>
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
                    description: getFirst(category.data),
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
      <Paginator page={page} lastPage={lastPage} />
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
  }, false);
  const subres = await api(null, 'categories.get', { locale }, false);

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
