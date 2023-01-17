import { useState, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import Link from 'next/link'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import { displaySet } from '../../redux/actions/main'
import { postsGet } from '../../redux/actions/posts'
import api from '../../lib/api'
import PostsGrid from '../../components/CardGrid'
import PostsFeed from '../../components/CardFeed'


export default () => {
    const dispatch = useDispatch()
    const system = useSelector((state) => state.system)
    const main = useSelector((state) => state.main)
    const posts = useSelector((state) => state.posts)
    const [loaded, setLoaded] = useState(null)

    const getPost = (data={}) => {
        api(main, 'posts.get', data).then(res => {
            if (res.posts) {
                dispatch(postsGet(res.posts))
            }
        })
    }

    useEffect(() => {
        if (system.prepared) {
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
        }
    }, [system.prepared])

    return (
        <>
            <div className="row">
                <div className="col-8">
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
                <div className="col-4" style={{ textAlign: 'right' }}>
                    <Link href="/posts/add">
                        <button
                            type="button"
                            className="btn btn-success"
                        >
                            <FontAwesomeIcon icon="fa-solid fa-plus" />
                        </button>
                    </Link>
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
