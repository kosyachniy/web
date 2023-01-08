import { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useRouter } from 'next/router'
import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import styles from '../../styles/edit.module.css'
import api from '../../functions/api'
import Editor from '../../components/Editor'


export default ({ post, setEdit, setPost }) => {
    const router = useRouter()
    const { t } = useTranslation('common')
    const main = useSelector((state) => state.main)
    const [title, setName] = useState(post ? post.title : '')
    const [data, setData] = useState(post ? post.data : '')
    const [editorLoaded, setEditorLoaded] = useState(false)
    const [redirect, setRedirect] = useState(null)

    const editPost = () => {
        let req = { title, data }

        if (post) {
            req['id'] = post.id
        }

        api(main.token, main.locale, 'posts.save', req).then(res => {
            if (res === 'save') {
                // TODO: notify about no access
                setEdit(false)
            } else if (post) {
                setPost(null)
                setEdit(false)
            } else {
                setRedirect(res.id)
            }
        })
    }

    useEffect(() => {
        setEditorLoaded(true)
    }, [])

    if (redirect) {
        router.push(`/posts/${redirect}`)
    }

    return (
        <div>
            <div className="album py-5">
                <div className="input-group mb-3">
                    <input
                        type="text"
                        className={ `form-control ${styles.title}` }
                        placeholder={ t('posts.title') }
                        value={ title }
                        onChange={ (event) => {setName(event.target.value)} }
                    />
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
                    onClick={ editPost }
                >
                    <FontAwesomeIcon icon="fa-regular fa-floppy-disk" />
                </button>
            </div>
        </div>
    )
}

export const getStaticProps = async ({ locale }) => ({
    props: {
        ...await serverSideTranslations(locale, ['common']),
    },
})
