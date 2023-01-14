import { useTranslation } from 'next-i18next'

import styles from '../styles/avatar.module.css'
import upload from '../lib/upload'


export default ({ image, setImage }) => {
    const { t } = useTranslation('common')

    const handleAvatar = (_e) => {
        const image = _e.target.files[0]
        upload(image).then((link) => {
            setImage(link)
        })
    }

    return (
        <div className={ styles.avatar }>
            <label htmlFor="avatar-loader">
                { image ? (
                    <img
                        src={ image }
                        alt={ t('profile.avatar') }
                    />
                ) : (
                    <div>{ t('system.upload') }</div>
                ) }

                <input
                    id="avatar-loader"
                    type="file"
                    accept="image/jpeg, image/png"
                    onChange={ (_e) => {handleAvatar(_e)} }
                />
            </label>
        </div>
    )
}
