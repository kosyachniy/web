import { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useRouter } from 'next/router'
import { useTranslation } from 'next-i18next'
// import MathJax from 'react-mathjax-preview'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import styles from '../../styles/post.module.css'
import api from '../../lib/api'
import Editor from '../Editor'


export const Edit = ({ post, setEdit, setPost }) => {
    const { t } = useTranslation('common')
    const router = useRouter()
    const main = useSelector(state => state.main)
    const [title, setTitle] = useState(post ? post.title : '')
    const [data, setData] = useState(post ? post.data : '')
    const [editorLoaded, setEditorLoaded] = useState(false)
    const [redirect, setRedirect] = useState(null)

    const editPost = () => {
        let req = { title, data }

        if (post) {
            req['id'] = post.id
        }

        api(main, 'posts.save', req).then(res => {
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
                        onChange={ event => setTitle(event.target.value) }
                    />
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
                    onClick={ editPost }
                >
                    <FontAwesomeIcon icon="fa-regular fa-floppy-disk" />
                </button>
            </div>
        </div>
    )
}

export default ({ id }) => {
    const router = useRouter()
    const system = useSelector(state => state.system)
    const main = useSelector(state => state.main)
    const profile = useSelector(state => state.profile)
    const [post, setPost] = useState(null)
    const [edit, setEdit] = useState(false)
    const [deleted, setDeleted] = useState(false)

    const getPost = (data={}) => api(main, 'posts.get', data).then(res => {
        if (res.posts) {
            setPost(res.posts)
        }
    })

    const deletePost = () => api(main, 'posts.rm', {id: post.id}).then(
        res => setDeleted(true)
    )

    useEffect(() => {
        if (system.prepared && !post) {
            getPost({ id })
        }
    }, [system.prepared, post])

    if (deleted) {
        router.push(`/`)
    }

    if (!post) {
        return (
            <></>
        )
    }

    return (
        <div className={ `album py-2 ${styles.post}` }>
            <div className="row">
                <div className="col-md-8">
                    <h1>{ post.title }</h1>
                </div>
                <div className="col-md-4" style={{ textAlign: 'right' }}>
                    { profile.status >= 2 && (<>
                        { edit ? (
                            <button
                                className="btn btn-outline-secondary"
                                onClick={ () => setEdit(false) }
                            >
                                <FontAwesomeIcon icon="fa-regular fa-eye" />
                            </button>
                        ) : (
                            <button
                                className="btn btn-outline-secondary"
                                onClick={ () => setEdit(true) }
                            >
                                <FontAwesomeIcon icon="fa-solid fa-pencil" />
                            </button>
                        ) }
                        <button
                            className="btn btn-danger"
                            onClick={ deletePost }
                        >
                            <FontAwesomeIcon icon="fa-solid fa-trash" />
                        </button>
                    </>) }
                </div>
            </div>

            { edit ? (
                <Edit
                    post={ post }
                    setEdit={ setEdit }
                    setPost={ setPost }
                />
            ) : (
                <>
                    { post.image && <img src={ post.image } alt={ post.title } /> }

                    <div dangerouslySetInnerHTML={{ __html: post.data }} />
                    {/*
                    <MathJax
                        math={ post.data }
                        sanitizeOptions={{
                            USE_PROFILES: {
                                html: true,
                                mathMl: true,
                            }
                        }}
                    />
                    */}

                    {/* <div style={{ marginTop: '50px', height: '250px' }}>
                        { post.geo ? (
                            <Map center={ post.geo} zoom={ 14 } />
                        ) : (
                            <Map />
                        )}
                    </div> */}
                </>
            ) }
        </div>
    )
}
