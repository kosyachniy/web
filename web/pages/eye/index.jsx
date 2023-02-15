import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import { useRouter } from 'next/router';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';

import { categoriesAdd } from '../../redux/actions/categories';
import { Online } from '../../components/Online';
import Category from '../../components/Category';

const List = ({
  categories, edit, setEdit, indent = 0,
}) => (
  <>
    { categories && categories.map(category => (
      <React.Fragment key={category.id}>
        <Category
          category={category}
          edit={edit === category.id}
          setEdit={setEdit}
          indent={indent}
        />
        <List
          categories={category.categories}
          edit={edit}
          setEdit={setEdit}
          indent={indent + 1}
        />
      </React.Fragment>
    )) }
  </>
);

const Container = ({
  main, profile, categories,
  categoriesAdd,
}) => {
  const { t } = useTranslation('common');
  const router = useRouter();
  const [edit, setEdit] = useState(null);

  const addCategory = () => {
    categoriesAdd({
      id: 0,
      title: '',
      data: null,
      parent: null,
      locale: main.locale,
    });
    setEdit(0);
  };

  useEffect(() => {
    if (main.token && profile.status < 6) {
      router.push('/');
    }
  }, [main.token]);

  return (
    <>
      <br />
      <Online />
      <br />
      <h1>{ t('system.categories') }</h1>
      <div className="accordion" id="accordionCategories">
        <List
          categories={categories}
          edit={edit}
          setEdit={setEdit}
        />
      </div>
      { edit !== 0 && (
        <button
          type="button"
          className="btn btn-success mt-3"
          style={{ width: '100%' }}
          onClick={addCategory}
        >
          <i className="fa-solid fa-plus" />
        </button>
      ) }
    </>
  );
};

export default connect(state => state, { categoriesAdd })(Container);

export const getStaticProps = async ({ locale }) => ({
  props: {
    ...await serverSideTranslations(locale, ['common']),
  },
});
