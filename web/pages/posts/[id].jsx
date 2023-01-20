import { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import api from '../../lib/api'
import Post from '../../components/Post'
import { Posts } from './'


export default ({ id }) => {
    const system = useSelector(state => state.system)
    const main = useSelector(state => state.main)
    const isPost = !isNaN(id.split('-').pop())
    const [category, setCategory] = useState(null)
    const [post, setPost] = useState(null)

    if (isPost) {
        id = +id.split('-').pop()
    }

    const getCategory = (data={}) => api(main, 'categories.get', data).then(
        res => res.categories && setCategory(res.categories)
    )

    const getPost = (data={}) => api(main, 'posts.get', data).then(
        res => res.posts && setPost(res.posts)
    )

    if (isPost) {
        useEffect(() => {
            system.prepared && (!post || +id !== post.id) && getPost({ id })
        }, [system.prepared, post, id])

        return (
            <Post post={ post } setPost={ setPost } />
        )
    } else {
        useEffect(() => {
            system.prepared && (!category || id !== category.url) && getCategory({ url: id })
        }, [system.prepared, category, id])

        if (!category) {
            return (
                <>
                    404 Not Found
                </>
            )
        }

        return (
            <Posts category={ category } />
        )
    }
}

export const getServerSideProps = async ({ query, locale }) => ({
    props: {
        id: query.id,
        ...await serverSideTranslations(locale, ['common']),
    },
})
