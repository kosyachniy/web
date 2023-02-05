import { useState, useEffect } from 'react'
import { connect } from 'react-redux'
import Link from 'next/link'
import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import styles from '../../styles/post.module.css'
import { toastAdd } from '../../redux/actions/system'
import { displaySet } from '../../redux/actions/main'
import api from '../../lib/api'
import Grid from '../../components/Post/Grid'
import Feed from '../../components/Post/Feed'
import Paginator from '../../components/Paginator'


const getPage = count => Math.floor(count / 18) + Boolean(count % 18)

export const Posts = ({
    system, main, profile,
    toastAdd, displaySet,
    category=null, page=1,
    postsLoaded=[], count=null,
}) => {
    const { t } = useTranslation('common')
    const [posts, setPosts] = useState(postsLoaded)
    const [lastPage, setLastPage] = useState(count ? getPage(count) : page)

    const getPost = (data={}) => api(main, 'posts.get', data).then(res => {
        if (res.posts) {
            setPosts(res.posts)
            res.count && setLastPage(getPage(res.count))
        }
    }).catch(err => toastAdd({
        header: t('system.error'),
        text: err,
        color: 'white',
        background: 'danger',
    }))

    useEffect(() => {
        system.prepared && getPost({
            category: category && category.id,
            locale: main.locale,
            search: system.search && system.search.length >= 3 ? system.search : '',
            limit: 18,
            offset: (page - 1) * 18,
        })
    }, [
        system.prepared,
        system.search && system.search.length >= 3 ? system.search : false,
        main.locale,
        category,
        page,
    ])

    return (
        <>
            <div className="row">
                <div className="col-8">
                    <h1>{ category ? category.title : t('structure.posts') }</h1>
                </div>
                <div className="col-4" style={{ textAlign: 'right' }}>
                    <div className="btn-group" role="group">
                        <button
                            type="button"
                            className={ `btn btn-${main.theme}` }
                            onClick={ () => displaySet('grid') }
                        >
                            <i className="fa-solid fa-table-cells-large" />
                        </button>
                        <button
                            type="button"
                            className={ `btn btn-${main.theme}` }
                        >
                            <i className="fa-solid fa-list-ul" />
                        </button>
                        <button
                            type="button"
                            className={ `btn btn-${main.theme}` }
                            onClick={ () => dispatch(displaySet('feed')) }
                        >
                            <i className="fa-regular fa-image" />
                        </button>
                    </div>
                    { profile.status >= 2 && (
                        <Link href="/posts/add">
                            <button
                                type="button"
                                className="btn btn-success ms-2"
                            >
                                <i className="fa-solid fa-plus" />
                            </button>
                        </Link>
                    ) }
                </div>
            </div>
            { category && (
                <>
                    { category.image && <img src={ category.image } alt={ category.title } className={ styles.image } /> }
                    <div dangerouslySetInnerHTML={{ __html: category.data }} />
                </>
            ) }
            {
                main.display == 'feed' ? (
                    <Feed posts={ posts } />
                ) : (
                    <Grid posts={ posts } />
                )
            }
            <Paginator page={ page } lastPage={ lastPage } />
        </>
    )
}

export default connect(state => state, { toastAdd, displaySet })(Posts)

export const getServerSideProps = async ({ query, locale }) => {
    const page = !isNaN(query.page) ? (+query.page || 1) : 1
    const res = await api(null, 'posts.get', {
        locale: locale,
        limit: 18,
        offset: (page - 1) * 18,
    }, false, false)

    return {
        props: {
            ...await serverSideTranslations(locale, ['common']),
            page,
            postsLoaded: res.posts || [],
            count: res.count,
        },
    }
}
