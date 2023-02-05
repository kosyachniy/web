import { useState, useEffect } from 'react'
import { connect } from 'react-redux'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import { toastAdd } from '../../redux/actions/system'
import { displaySet } from '../../redux/actions/main'
import api from '../../lib/api'
import Post from '../../components/Post'
import { Posts } from './'


const Container = ({
    system, main, profile,
    toastAdd, displaySet,
    isPost, id, postLoaded, categoryLoaded, page, postsLoaded, count,
}) => {
    const [category, setCategory] = useState(categoryLoaded)
    const [post, setPost] = useState(postLoaded)

    const getCategory = (data={}) => api(main, 'categories.get', data).then(
        res => res.categories && setCategory(res.categories)
    ).catch(err => toastAdd({
        header: t('system.error'),
        text: err,
        color: 'white',
        background: 'danger',
    }))

    const getPost = (data={}) => api(main, 'posts.get', data).then(
        res => res.posts && setPost(res.posts)
    ).catch(err => toastAdd({
        header: t('system.error'),
        text: err,
        color: 'white',
        background: 'danger',
    }))

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
            <Posts { ...{
                system, main, profile,
                toastAdd, displaySet,
                category, page,
                postsLoaded, count,
            } } />
        )
    }
}


export default connect(state => state, { toastAdd, displaySet })(Container)

export const getServerSideProps = async ({ query, locale }) => {
    let id = query.id
    const isPost = !isNaN(id.split('-').pop())

    let postLoaded = null
    let categoryLoaded = null
    let page = null
    let postsLoaded = []
    let count = null

    if (isPost) {
        id = +id.split('-').pop()
        const res = await api(null, 'posts.get', { id }, false)
        postLoaded = res.posts || null
    } else {
        const res = await api(null, 'categories.get', { url: id }, false)
        categoryLoaded = res.categories || null

        page = !isNaN(query.page) ? (+query.page || 1) : 1
        const subres = await api(null, 'posts.get', {
            category: categoryLoaded && categoryLoaded.id,
            locale: locale,
            limit: 18,
            offset: (page - 1) * 18,
        }, false)
        postsLoaded = subres.posts || null
        count = subres.count
    }

    return {
        props: {
            ...await serverSideTranslations(locale, ['common']),
            isPost, id, postLoaded, categoryLoaded, page, postsLoaded, count,
        },
    }
}
