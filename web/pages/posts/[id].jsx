import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import Post from '../../components/Post'


export default ({ id }) => (
    <Post id={ id } />
)

export const getServerSideProps = async ({ query, locale }) => ({
    props: {
        id: query.id,
        ...await serverSideTranslations(locale, ['common']),
    },
})
