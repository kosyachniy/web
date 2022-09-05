import { useState, useEffect } from 'react'
import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { useSelector } from 'react-redux'
import Link from 'next/link'
// import MathJax from 'react-mathjax-preview'

import api from '../../functions/api'


export const getServerSideProps = async ({ query }) => {
    return {
        props: {
            id: query['id'],
        }
    }
}

export default ({ id }) => {
    const { t } = useTranslation('common')
    const system = useSelector((state) => state.system)
    const [post, setPost] = useState(null)
    const [edit, setEdit] = useState(false)
    const [deleted, setDeleted] = useState(false)

    const getPost = (data={}) => {
        api(system.token, system.locale, 'posts.get', data).then(res => {
            setPost(res['posts'])
        })
    }

    const deletePost = () => {
        const data = {
            id: post.id,
        }

        api(system.token, system.locale, 'posts.delete', data).then(res => {
            setDeleted(true)
        })
    }

    useEffect(() => {
        getPost({ id })
    }, [])

    // if (deleted) {
    //     return (
    //         <Navigate to="/" />
    //     )
    // }

    if (!post) {
        return (
            <></>
        )
    }

    return (
        <div id="post">
            <div className="album py-2">
                <h1>{ post.title }</h1>

                { edit ? (
                    <button
                        className="btn btn-outline-secondary"
                        onClick={ () => {setEdit(false)} }
                    >
                        <i className="far fa-eye" />
                    </button>
                ) : (
                    <button
                        className="btn btn-outline-secondary"
                        onClick={ () => {setEdit(true)} }
                    >
                        <i className="bi bi-pencil-fill" />
                    </button>
                ) }
                <button
                    className="btn btn-danger"
                    onClick={ deletePost }
                >
                    <i className="far fa-trash-alt" />
                </button>

                { edit ? (
                    <Edit
                        post={ post }
                        handlerSave={ savePost }
                    />
                ) : (
                    <>
                        { post.cover ? (
                            <img
                                src={ post.cover }
                                alt={ post.title }
                            />
                        ) : (<></>) }
                        <br /><br />
                        { post.data }
                        {/* <MathJax
                            math={ post.data }
                            sanitizeOptions={{
                                USE_PROFILES: {
                                    html: true,
                                    mathMl: true,
                                }
                            }}
                        /> */}

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

export const getStaticProps = async ({ locale }) => ({
    props: {
        ...await serverSideTranslations(locale, ['common']),
    },
})
