import { serverSideTranslations } from 'next-i18next/serverSideTranslations';

import api from '../lib/api';
import Posts from './posts';

export default Posts;

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
