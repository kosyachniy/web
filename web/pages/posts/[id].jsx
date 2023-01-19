import { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import api from '../../lib/api'
import Post from '../../components/Post'


export default ({ id }) => {
    const system = useSelector(state => state.system)
    const main = useSelector(state => state.main)
    const [post, setPost] = useState(null)

    const getPost = (data={}) => api(main, 'posts.get', data).then(
        res => res.posts && setPost(res.posts)
    )

    useEffect(() => {
        if (system.prepared && (!post || +id !== post.id)) {
            getPost({ id })
        }
    }, [system.prepared, post])

    return (
        <Post post={ post } setPost={ setPost } />
    )
}

export const getServerSideProps = async ({ query, locale }) => ({
    props: {
        id: query.id,
        ...await serverSideTranslations(locale, ['common']),
    },
})
