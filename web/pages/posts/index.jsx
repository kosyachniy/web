import { useState, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import Link from 'next/link'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import { postsGet, displaySet } from '../../store'
import api from '../../functions/api'
import PostsGrid from '../../components/CardGrid'
import PostsFeed from '../../components/CardFeed'


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
            getPost({ search: system.search })
        }
    })

    return (
        <>
            <div className="row">
                <div className="col-xs-10 col-sm-10 col-md-10">
                    <div className="btn-group" role="group" >
                        <button
                            type="button"
                            className={ `btn btn-${system.theme}` }
                            onClick={ () => {dispatch(displaySet('grid'))}}
                        >
                            <i className="fas fa-th-large"></i>
                        </button>
                        <button
                            type="button"
                            className={ `btn btn-${system.theme}` }
                        >
                            <i className="fas fa-th-list"></i>
                        </button>
                        <button
                            type="button"
                            className={ `btn btn-${system.theme}` }
                            onClick={ () => {dispatch(displaySet('feed'))}}
                        >
                            <i className="fas fa-image"></i>
                        </button>
                    </div>
                </div>
                <div className="col-xs-2 col-sm-2 col-md-2" style={{ textAlign: 'right' }}>
                    <div className="btn-group">
                        <Link href="/posts/add">
                            <button
                                type="button"
                                className="btn btn-success"
                                style={{ width: '100%' }}
                            >
                                <i className="fas fa-plus" />
                            </button>
                        </Link>
                    </div>
                </div>
            </div>
            {
                system.display == 'feed' ? (
                    <PostsFeed posts={ posts } />
                ) : (
                    <PostsGrid posts={ posts } />
                )
            }
        </>
    )
}

export const getStaticProps = async ({ locale }) => ({
    props: {
        ...await serverSideTranslations(locale, ['common']),
    },
})
