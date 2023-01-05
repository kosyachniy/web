import { useState, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import Link from 'next/link'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import { displaySet } from '../../redux/actions/main'
import { postsGet } from '../../redux/actions/posts'
import api from '../../functions/api'
import PostsGrid from '../../components/CardGrid'
import PostsFeed from '../../components/CardFeed'


export default () => {
    const dispatch = useDispatch()
    const system = useSelector((state) => state.system)
    const main = useSelector((state) => state.main)
    const posts = useSelector((state) => state.posts)
    const [loaded, setLoaded] = useState(null)

    const getPost = (data={}) => {
        api(main.token, main.locale, 'posts.get', data).then(res => {
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
                            className={ `btn btn-${main.theme}` }
                            onClick={ () => {dispatch(displaySet('grid'))}}
                        >
                            <FontAwesomeIcon icon="fa-solid fa-table-cells-large" />
                        </button>
                        <button
                            type="button"
                            className={ `btn btn-${main.theme}` }
                        >
                            <FontAwesomeIcon icon="fa-solid fa-list-ul" />
                        </button>
                        <button
                            type="button"
                            className={ `btn btn-${main.theme}` }
                            onClick={ () => {dispatch(displaySet('feed'))}}
                        >
                            <FontAwesomeIcon icon="fa-regular fa-image" />
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
                                <FontAwesomeIcon icon="fa-solid fa-plus" />
                            </button>
                        </Link>
                    </div>
                </div>
            </div>
            {
                main.display == 'feed' ? (
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
