import { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';

import { toastAdd } from '../../redux/actions/system';
import { displaySet } from '../../redux/actions/main';
import api from '../../lib/api';
import Post from '../../components/Post';
import { Posts } from '.';

const Container = ({
  system, main, profile,
  toastAdd, displaySet,
  isPost, id, postLoaded, categoryLoaded, page, postsLoaded, count,
}) => {
  const { t } = useTranslation('common');
  const [category, setCategory] = useState(categoryLoaded);
  const [post, setPost] = useState(postLoaded);
  const [viewed, setViewed] = useState(false);

  const getCategory = (data = {}) => api(main, 'categories.get', data).then(
    res => res.categories && setCategory(res.categories),
  ).catch(err => toastAdd({
    header: t('system.error'),
    text: err,
    color: 'white',
    background: 'danger',
  }));

  const getPost = (data = {}) => api(main, 'posts.get', data).then(
    res => res.posts && setPost(res.posts),
  ).catch(err => toastAdd({
    header: t('system.error'),
    text: err,
    color: 'white',
    background: 'danger',
  }));

  if (isPost) {
    useEffect(() => {
      if (main.token && (!viewed || !post || +id !== post.id)) {
        setPost(null);
        getPost({ id, utm: main.utm });
        setViewed(true);
      }
    }, [main.token, post, id]);

    return (
      <Post post={post} setPost={setPost} />
    );
  }

  useEffect(() => {
    if (main.token && (!category || id !== category.url)) {
      getCategory({ url: id });
    }
  }, [main.token, category, id]);

  if (!category) {
    return null;
  }

  return (
    <Posts {...{
      system,
      main,
      profile,
      toastAdd,
      displaySet,
      category,
      page,
      postsLoaded,
      count,
      subcategories: categoryLoaded ? categoryLoaded.categories : [],
    }}
    />
  );
};

export default connect(state => state, { toastAdd, displaySet })(Container);

export const getServerSideProps = async ({ query, locale }) => {
  let { id } = query;
  const isPost = !Number.isNaN(Number(id.split('-').pop()));

  let postLoaded = null;
  let categoryLoaded = null;
  let page = null;
  let postsLoaded = [];
  let count = null;

  if (isPost) {
    id = +id.split('-').pop();
    try {
      const res = await api(null, 'posts.get', { id }, false, true);
      postLoaded = res.posts || null;
    } catch {
      postLoaded = null;
    }
  } else {
    try {
      const res = await api(null, 'categories.get', { url: id }, false, true);
      categoryLoaded = res.categories || null;

      page = !Number.isNaN(Number(query.page)) ? (+query.page || 1) : 1;
      const subres = await api(null, 'posts.get', {
        category: categoryLoaded && categoryLoaded.id,
        locale,
        limit: 18,
        offset: (page - 1) * 18,
      }, false, true);
      postsLoaded = subres.posts || null;
      count = subres.count;
    } catch {
      categoryLoaded = null;
      postsLoaded = null;
      count = 0;
    }
  }

  return {
    props: {
      ...await serverSideTranslations(locale, ['common']),
      isPost,
      id,
      postLoaded,
      categoryLoaded,
      page,
      postsLoaded,
      count,
    },
  };
};
