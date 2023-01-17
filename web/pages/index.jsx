import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import Posts from './posts'


export default () => (
    <Posts />
)

export const getStaticProps = async ({ locale }) => ({
    props: {
        ...await serverSideTranslations(locale, ['common']),
    },
})
