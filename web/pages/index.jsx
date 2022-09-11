import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import Posts from './posts'


export default () => {
    return (
        <Posts />
    )
}

export const getStaticProps = async ({ locale }) => ({
    props: {
        ...await serverSideTranslations(locale, ['common']),
    },
})
