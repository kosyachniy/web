import { useState, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import Link from 'next/link'
import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import { displaySet } from '../../redux/actions/main'
import api from '../../lib/api'
import Grid from '../../components/Post/Grid'
import Feed from '../../components/Post/Feed'


export default () => {
    const { t } = useTranslation('common')
    const dispatch = useDispatch()
    const system = useSelector(state => state.system)
    const main = useSelector(state => state.main)
    const profile = useSelector(state => state.profile)
    const [posts, setPosts] = useState([])

    const getPost = (data={}) => api(main, 'posts.get', data).then(
        res => res.posts && setPosts(res.posts)
    )

    useEffect(() => {
        system.prepared && getPost({ locale: main.locale, search: system.search })
    }, [
        system.prepared,
        system.search && system.search.length >= 3 ? system.search : false,
        main.locale,
    ])

    return (
        <>
            <div className="row">
                <div className="col-8">
                    <h1>{ t('structure.posts') }</h1>
                </div>
                <div className="col-4" style={{ textAlign: 'right' }}>
                    <div className="btn-group" role="group">
                        <button
                            type="button"
                            className={ `btn btn-${main.theme}` }
                            onClick={ () => dispatch(displaySet('grid')) }
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
                            onClick={ () => dispatch(displaySet('feed')) }
                        >
                            <FontAwesomeIcon icon="fa-regular fa-image" />
                        </button>
                    </div>
                    { profile.status >= 2 && (
                        <Link href="/posts/add">
                            <button
                                type="button"
                                className="btn btn-success ms-2"
                            >
                                <FontAwesomeIcon icon="fa-solid fa-plus" />
                            </button>
                        </Link>
                    ) }
                </div>
            </div>
            {
                main.display == 'feed' ? (
                    <Feed posts={ posts } />
                ) : (
                    <Grid posts={ posts } />
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
