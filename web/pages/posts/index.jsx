import { useState, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import { postsGet } from '../../store'
import api from '../../functions/api'
import PostsGrid from '../../components/CardGrid'


export default () => {
    const dispatch = useDispatch()
    const system = useSelector((state) => state.system)
    const posts = useSelector((state) => state.posts)
    const [loaded, setLoaded] = useState(null)

    const getPost = (data={}) => {
        api(system.token, system.locale, 'posts.get', data).then(res => {
            dispatch(postsGet(res.posts))
        })
    }

    useEffect(() => {
        if (
            system.search !== loaded
            && (
                system.search === ''
                || system.search.length >= 3
            )
        ) {
            setLoaded(system.search)
            getPost({search: system.search})
        }
    })

    return (
        <PostsGrid posts={ posts } />
    )
}

export const getStaticProps = async ({ locale }) => ({
    props: {
        ...await serverSideTranslations(locale, ['common']),
    },
})
