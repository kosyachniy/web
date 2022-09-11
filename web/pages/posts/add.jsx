import { useState } from 'react'
import { useSelector } from 'react-redux'
import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import styles from '../../styles/edit.module.css'
import api from '../../functions/api'
// import { getPost } from './[id]'
// import Editor from '../../components/Editor'


export default ({ post }) => {
    const { t } = useTranslation('common')
    const system = useSelector((state) => state.system)
    const [title, setName] = useState(post ? post.title : '')
    const [data, setData] = useState(post ? post.data : '')
    const [redirect, setRedirect] = useState(null)

    const savePost = () => {
        getPost({ id: post.id })
        setEdit(false)
    }

    const editPost = () => {
        let req = { title, data }

        if (post) {
            req['id'] = post.id
        }

        api(system.token, system.locale, 'posts.save', req).then(res => {
            if (post) {
                savePost()
            } else {
                setRedirect(res.id)
            }
        })
    }

    // if (redirect) {
    //     return (
    //         <Navigate to={ `/posts/${redirect}` } />
    //     )
    // }

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

                {/* <Editor
                    data={ data }
                    updatePost={ (text) => {setData(text)} }
                /> */}

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
