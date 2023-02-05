import { connect } from 'react-redux'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import { toastAdd } from '../redux/actions/system'
import { displaySet } from '../redux/actions/main'
import api from '../lib/api'
import Posts from './posts'


export default connect(state => state, { toastAdd, displaySet })(Posts)

export const getServerSideProps = async ({ query, locale }) => {
    const page = !isNaN(query.page) ? (+query.page || 1) : 1
    const res = await api(null, 'posts.get', {
        locale: locale,
        limit: 18,
        offset: (page - 1) * 18,
    }, false)

    return {
        props: {
            ...await serverSideTranslations(locale, ['common']),
            page,
            postsLoaded: res.posts || [],
            count: res.count,
        },
    }
}
