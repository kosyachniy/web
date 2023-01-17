import { useState, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
// import Link from 'next/link'
import { useTranslation } from 'next-i18next'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import styles from '../styles/card.module.css'
import api from '../lib/api'
import Editor from './Editor'


export default ({
    category,
    edit=false,
    setEdit=null,
    categories=[],
    setCategories=null,
}) => {
    // const router = useRouter()
    const { t } = useTranslation('common')
    const main = useSelector((state) => state.main)
    const [title, setTitle] = useState(category ? category.title : '')
    const [data, setData] = useState(category ? category.data : '')
    const [parent, setParent] = useState(category ? category.parent : null)
    const [editorLoaded, setEditorLoaded] = useState(false)

    const editCategory = () => {
        if (!title) {
            // TODO: notify
            return
        }

        let req = { title, data, parent }
        if (category) {
            req['id'] = category.id
        }

        api(main, 'categories.save', req).then(res => {
            if (res === 'save') {
                // TODO: notify about no access
            }
            setEdit(null)
            setCategories([])
        })
    }

    useEffect(() => {
        setEditorLoaded(true)
    }, [])

    if (!edit) {
        return (
            <>
                { category.title }
            </>
        )
    }

    return (
        <div>
            <div className="album py-5">
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
                        onChange={ event => setParent(event.target.value)}
                    >
                        <option defaultValue>{ t('categories.top') }</option>
                        { categories.map(cat => cat.id && (
                            <option value={ cat.id } key={ cat.id }>
                                { cat.title }
                            </option>
                        )) }
                    </select>
                </div>
                <Editor
                    editorLoaded={ editorLoaded }
                    data={ data }
                    updatePost={ (text) => {setData(text)} }
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
        </div>
    )
}
