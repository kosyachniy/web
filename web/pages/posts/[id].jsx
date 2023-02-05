import { useState, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import wrapper from '../../redux/store';
import { toastAdd } from '../../redux/actions/system'
import api from '../../lib/api'
import Post from '../../components/Post'
import { Posts } from './'


export default ({ id }) => {
    const dispatch = useDispatch()
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
    ).catch(err => dispatch(toastAdd({
        header: t('system.error'),
        text: err,
        color: 'white',
        background: 'danger',
    })))

    const getPost = (data={}) => api(main, 'posts.get', data).then(
        res => res.posts && setPost(res.posts)
    ).catch(err => dispatch(toastAdd({
        header: t('system.error'),
        text: err,
        color: 'white',
        background: 'danger',
    })))

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
                <></>
            )
        }

        return (
            <Posts category={ category } />
        )
    }
}

export const getServerSideProps = wrapper.getServerSideProps(store => async ({ query, locale }) => ({
    props: {
        id: query.id,
        ...await serverSideTranslations(locale, ['common']),
    },
}))
