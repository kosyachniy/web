import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useTranslation } from 'next-i18next';

import styles from '../styles/card.module.css';
import { toastAdd } from '../redux/actions/system';
import { categoriesClear } from '../redux/actions/categories';
import api from '../lib/api';
import Upload from './Forms/Upload';
import Locale from './Forms/Locale';
import Category from './Forms/Category';
import Editor from './Forms/Editor';

const Edit = ({
  category,
  setEdit = null,
}) => {
  const { t } = useTranslation('common');
  const dispatch = useDispatch();
  const main = useSelector(state => state.main);
  const [title, setTitle] = useState(category ? category.title : '');
  const [description, setDescription] = useState(category ? category.description : '');
  const [data, setData] = useState(category ? category.data : '');
  const [image, setImage] = useState(category ? category.image : null);
  const [parent, setParent] = useState(category ? category.parent : null);
  const [locale, setLocale] = useState(category ? category.locale : main.locale);
  const [editorLoaded, setEditorLoaded] = useState(false);

  const blockCategory = ({ status }) => api(main, 'categories.save', { id: category.id, status }).then(() => {
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

  const rmCategory = () => api(main, 'categories.rm', { id: category.id }).then(() => {
    setEdit(null);
    dispatch(categoriesClear());
    dispatch(toastAdd({
      header: t('system.success'),
      text: t('system.deleted'),
      color: 'white',
      background: 'success',
    }));
  }).catch(err => dispatch(toastAdd({
    header: t('system.error'),
    text: err,
    color: 'white',
    background: 'danger',
  })));

  const editCategory = () => {
    if (!title) {
      // TODO: notify
      return;
    }

    const req = {
      title, description, data, image, parent, locale,
    };
    if (category) {
      req.id = category.id;
    }

    api(main, 'categories.save', req).then(() => {
      setEdit(null);
      dispatch(categoriesClear());
      dispatch(toastAdd({
        header: t('system.success'),
        text: t('system.saved'),
        color: 'white',
        background: 'success',
      }));
    }).catch(err => dispatch(toastAdd({
      header: t('system.error'),
      text: err,
      color: 'white',
      background: 'danger',
    })));
  };

  useEffect(() => {
    setEditorLoaded(true);
  }, []);

  return (
    <div className="album">
      <div className="row py-3">
        <div className="col-6">
          { category.status ? (
            <button
              type="button"
              className="btn btn-danger"
              style={{ width: '100%' }}
              onClick={() => blockCategory({ status: 0 })}
            >
              <i className="fa-solid fa-lock" />
            </button>
          ) : (
            <button
              type="button"
              className="btn btn-success"
              style={{ width: '100%' }}
              onClick={() => blockCategory({ status: 1 })}
            >
              <i className="fa-solid fa-lock-open" />
            </button>
          )}
        </div>
        <div className="col-6">
          <button
            type="button"
            className="btn btn-danger"
            style={{ width: '100%' }}
            onClick={() => rmCategory()}
          >
            <i className="fa-solid fa-trash" />
          </button>
        </div>
      </div>
      <div className="input-group mb-3">
        <input
          type="text"
          className={`form-control ${styles.title}`}
          placeholder={t('categories.title')}
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
            category={parent}
            setCategory={setParent}
            exclude={category.id}
            custom={t('categories.parent')}
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
        onClick={editCategory}
      >
        <i className="fa-regular fa-floppy-disk" />
      </button>
    </div>
  );
};

export default ({
  category,
  edit = false,
  setEdit = null,
  indent = 0,
}) => (
  <div className="accordion-item">
    <h2 className="accordion-header" id={`heading${category.id}`}>
      <button
        className={`accordion-button ${!edit && 'collapsed'}`}
        type="button"
        data-bs-toggle="collapse"
        data-bs-target={`#collapse${category.id}`}
        aria-expanded={edit ? 'true' : 'false'}
        aria-controls={`collapse${category.id}`}
        onClick={() => setEdit(category.id)}
      >
        { indent ? (
          <>
            <div dangerouslySetInnerHTML={{ __html: '<div class="px-3 d-inline"></div>'.repeat(indent - 1) }} />
            <div className="px-3 d-inline text-secondary">↳</div>
          </>
        ) : (<></>) }
        <div className="text-secondary me-2">
          #
          { category.id }
          { !category.status && <i className="fa-solid fa-lock ms-2" /> }
        </div>
        { category.title }
      </button>
    </h2>
    <div
      id={`collapse${category.id}`}
      className={`accordion-collapse collapse ${edit && 'show'}`}
      aria-labelledby={`heading${category.id}`}
      data-bs-parent="#accordionCategories"
    >
      <div className="accordion-body">
        { edit && (
          <Edit
            category={category}
            setEdit={setEdit}
          />
        ) }
      </div>
    </div>
  </div>
);
