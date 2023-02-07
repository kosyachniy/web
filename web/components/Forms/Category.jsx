import React from 'react';
import { useSelector } from 'react-redux';
import { useTranslation } from 'next-i18next';

const List = ({ categories, exclude, indent = 0 }) => (
  <>
    { categories && categories.map(category => category.id && category.id !== exclude && (
    <React.Fragment key={category.id}>
      <option value={category.id}>
        <div dangerouslySetInnerHTML={{ __html: '&nbsp;&nbsp;&nbsp;'.repeat(indent) }} />
        #
        { category.id }
&nbsp;&nbsp;
        { category.title }
      </option>
      <List
        categories={category.categories}
        exclude={exclude}
        indent={indent + 1}
      />
    </React.Fragment>
    )) }
  </>
);

export default ({
  category, setCategory, exclude = null, custom = null,
}) => {
  const { t } = useTranslation('common');
  const categories = useSelector(state => state.categories);

  return (
    <div className="input-group mb-3">
      <label className="input-group-text" htmlFor="category">
        { custom || t('categories.category') }
      </label>
      <select
        className="form-select"
        id="category"
        value={category || '0'}
        onChange={event => setCategory(event.target.value)}
      >
        <option value="0" defaultValue>{ t('categories.top') }</option>
        <List categories={categories} exclude={exclude} />
      </select>
    </div>
  );
};
