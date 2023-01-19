import { useState, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { useTranslation } from 'next-i18next'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import styles from '../styles/card.module.css'
import { categoriesClear } from '../redux/actions/categories'
import api from '../lib/api'
import Editor from './Editor'


const List = ({ categories, current, indent=0 }) => (
    <>
        { categories && categories.map(category => category.id && category.id != current.id && (
            <>
                <option
                    value={ category.id }
                    key={ category.id }
                    selected={ category.id === current.parent ? true : false }
                >
                    <div dangerouslySetInnerHTML={{ __html: `&nbsp;&nbsp;&nbsp;`.repeat(indent) }} />
                    #{ category.id }&nbsp;&nbsp;
                    { category.title }
                </option>
                <List
                    categories={ category.categories }
                    current={ current }
                    indent={ indent + 1 }
                />
            </>
        )) }
    </>
)

const Edit = ({
    category,
    setEdit=null,
}) => {
    const { t } = useTranslation('common')
    const dispatch = useDispatch()
    const main = useSelector(state => state.main)
    const categories = useSelector(state => state.categories)
    const [title, setTitle] = useState(category ? category.title : '')
    const [data, setData] = useState(category ? category.data : '')
    const [parent, setParent] = useState(category ? category.parent : null)
    const [locale, setLocale] = useState(category ? category.locale : main.locale)
    const [editorLoaded, setEditorLoaded] = useState(false)

    const editCategory = () => {
        if (!title) {
            // TODO: notify
            return
        }

        let req = { title, data, parent, locale }
        if (category) {
            req['id'] = category.id
        }

        api(main, 'categories.save', req).then(res => {
            if (res === 'save') {
                // TODO: notify about no access
            }
            setEdit(null)
            dispatch(categoriesClear())
        })
    }

    useEffect(() => {
        setEditorLoaded(true)
    }, [])

    return (
        <div className="album">
            <div className="input-group mb-3">
                <input
                    type="text"
                    className={ `form-control ${styles.title}` }
                    placeholder={ t('categories.title') }
                    value={ title }
                    onChange={ event => setTitle(event.target.value) }
                />
            </div>
            <div className="input-group mb-3">
                <label className="input-group-text" htmlFor="categoryParent">
                    { t('categories.parent') }
                </label>
                <select
                    className="form-select"
                    id="categoryParent"
                    onChange={ event => setParent(event.target.value) }
                >
                    <option value="0" defaultValue>{ t('categories.top') }</option>
                    <List categories={ categories } current={ category } />
                </select>
            </div>
            <div className="input-group mb-3">
                <label className="input-group-text" htmlFor="categoryLocale">
                    { t('system.locale') }
                </label>
                <select
                    className="form-select"
                    id="categoryLocale"
                    onChange={ event => setLocale(event.target.value) }
                >
                    <option value="" defaultValue>🌎 { t('system.worldwide') }</option>
                    <option value="en" selected={ locale == 'en' }>🇬🇧 English</option>
                    <option value="ru" selected={ locale == 'ru' }>🇷🇺 Русский</option>
                </select>
            </div>
            <Editor
                editorLoaded={ editorLoaded }
                data={ data }
                updatePost={ text => setData(text) }
            />
            <br />
            <button
                className="btn btn-success"
                style={{ width: '100%' }}
                onClick={ editCategory }
            >
                <FontAwesomeIcon icon="fa-regular fa-floppy-disk" />
            </button>
        </div>
    )
}

export default ({
    category,
    edit=false,
    setEdit=null,
    indent=0,
}) => (
    <div className="accordion-item">
        <h2 className="accordion-header" id={ `heading${category.id}` }>
            <button
                className={ `accordion-button ${ !edit && "collapsed" }` }
                type="button"
                data-bs-toggle="collapse"
                data-bs-target={ `#collapse${category.id}` }
                aria-expanded={ edit ? "true" : "false" }
                aria-controls={ `collapse${category.id}` }
                onClick={ () => setEdit(category.id) }
            >
                { indent ? (
                    <>
                        <div dangerouslySetInnerHTML={{ __html: `<div class="px-3 d-inline"></div>`.repeat(indent - 1) }} />
                        <div className="px-3 d-inline text-secondary">↳</div>
                    </>
                ) : (<></>) }
                <div className="text-secondary me-2">#{ category.id }</div>
                { category.title }
            </button>
        </h2>
        <div
            id={ `collapse${category.id}` }
            className={ `accordion-collapse collapse ${ edit && "show" }` }
            aria-labelledby={ `heading${category.id}` }
            data-bs-parent="#accordionCategories"
        >
            <div className="accordion-body">
                { edit &&
                    <Edit
                        category={category}
                        setEdit={setEdit}
                    />
                }
            </div>
        </div>
    </div>
)
