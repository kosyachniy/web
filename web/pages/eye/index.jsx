import React, { useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { useRouter } from 'next/router'
import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import { categoriesAdd } from '../../redux/actions/categories'
import Category from '../../components/Category'


const List = ({ categories, edit, setEdit, indent=0 }) => (
    <>
        { categories && categories.map(category => (
            <React.Fragment key={ category.id }>
                <Category
                    category={ category }
                    edit={ edit === category.id }
                    setEdit={ setEdit }
                    indent={ indent }
                />
                <List
                    categories={ category.categories }
                    edit={ edit }
                    setEdit={ setEdit }
                    indent={ indent + 1 }
                />
            </React.Fragment>
        )) }
    </>
)

export default () => {
    const { t } = useTranslation('common')
    const dispatch = useDispatch()
    const router = useRouter()
    const main = useSelector(state => state.main)
    const profile = useSelector(state => state.profile)
    const categories = useSelector(state => state.categories)
    const [edit, setEdit] = useState(null)

    const addCategory = () => {
        dispatch(categoriesAdd({
            id: 0,
            title: '',
            data: null,
            parent: null,
            locale: main.locale,
        }))
        setEdit(0)
    }

    if (profile.status < 6) {
        router.push("/")
    }

    return (
        <>
            <h1>{ t('system.categories') }</h1>
            <div className="accordion" id="accordionCategories">
                <List
                    categories={ categories }
                    edit={ edit }
                    setEdit={ setEdit }
                />
            </div>
            { edit !== 0 && (
                <button
                    type="button"
                    className="btn btn-success mt-3"
                    style={{ width: '100%' }}
                    onClick={ addCategory }
                >
                    <i className="fa-solid fa-plus" />
                </button>
            ) }
        </>
    )
}

export const getStaticProps = async ({ locale }) => ({
    props: {
        ...await serverSideTranslations(locale, ['common']),
    },
})
