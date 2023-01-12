import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
// import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { useSelector } from 'react-redux'
import MathJax from 'react-mathjax-preview'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import styles from '../../styles/post.module.css'
import api from '../../lib/api'
import Edit from './add'


export default ({ id }) => {
    const router = useRouter()
    // const { t } = useTranslation('common')
    const system = useSelector((state) => state.system)
    const main = useSelector((state) => state.main)
    const [post, setPost] = useState(null)
    const [edit, setEdit] = useState(false)
    const [deleted, setDeleted] = useState(false)

    const getPost = (data={}) => {
        api(main, 'posts.get', data).then(res => {
            if (res.posts) {
                setPost(res.posts)
            }
        })
    }

    const deletePost = () => {
        const data = {
            id: post.id,
        }

        api(main, 'posts.rm', data).then(res => {
            setDeleted(true)
        })
    }

    useEffect(() => {
        if (system.prepared && !post) {
            getPost({ id })
        }
    }, [system.prepared])

    if (deleted) {
        router.push(`/`)
    }

    if (!post) {
        return (
            <></>
        )
    }

    return (
        <div className={ styles.post }>
            <div className="album py-2">
                <div className="row">
                    <div className="col-md-8">
                        <h1>{ post.title }</h1>
                    </div>
                    <div className="col-md-4" style={{ textAlign: 'right' }}>
                        { edit ? (
                            <button
                                className="btn btn-outline-secondary"
                                onClick={ () => {setEdit(false)} }
                            >
                                <FontAwesomeIcon icon="fa-regular fa-eye" />
                            </button>
                        ) : (
                            <button
                                className="btn btn-outline-secondary"
                                onClick={ () => {setEdit(true)} }
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
                        { post.image ? (
                            <img
                                src={ post.image }
                                alt={ post.title }
                            />
                        ) : (<></>) }
                        <br /><br />
                        <MathJax
                            math={ post.data }
                            sanitizeOptions={{
                                USE_PROFILES: {
                                    html: true,
                                    mathMl: true,
                                }
                            }}
                        />

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
        </div>
    )
}

export const getServerSideProps = async ({ query, locale }) => {
    return {
        props: {
            id: query.id,
            ...await serverSideTranslations(locale, ['common']),
        },
    }
}
