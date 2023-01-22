import { useState, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import Link from 'next/link'
import { useRouter } from 'next/router'
import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import styles from '../../styles/post.module.css'
import { toastAdd } from '../../redux/actions/system'
import { displaySet } from '../../redux/actions/main'
import api from '../../lib/api'
import Grid from '../../components/Post/Grid'
import Feed from '../../components/Post/Feed'
import Paginator from '../../components/Paginator'


export const Posts = ({ category=null }) => {
    const { t } = useTranslation('common')
    const dispatch = useDispatch()
    const router = useRouter()
    const system = useSelector(state => state.system)
    const main = useSelector(state => state.main)
    const profile = useSelector(state => state.profile)
    const page = !isNaN(router.query.page) ? (+router.query.page || 1) : 1
    const [posts, setPosts] = useState([])
    const [lastPage, setLastPage] = useState(page)

    const getPost = (data={}) => api(main, 'posts.get', data).then(res => {
        if (res.posts) {
            setPosts(res.posts)
            res.count && setLastPage(Math.floor(res.count / 18) + Boolean(res.count % 18))
        }
    }).catch(err => dispatch(toastAdd({
        header: t('system.error'),
        text: err,
        color: 'white',
        background: 'danger',
    })))

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
                            onClick={ () => dispatch(displaySet('grid')) }
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

export default () => <Posts />

export const getStaticProps = async ({ locale }) => ({
    props: {
        ...await serverSideTranslations(locale, ['common']),
    },
})
