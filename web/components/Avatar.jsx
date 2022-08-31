import { useState } from 'react'
import { useTranslation } from 'next-i18next'

import uploadImage from '../functions/upload'


export default ({ avatar }) => {
    const { t } = useTranslation('common')
    const [img, setImg] = useState(avatar)

    handleAvatar = (_e) => {
        const image = _e.target.files[0]
        uploadImage(image).then((link) => {
            setImg({ link })
            setAvatar(link)
        })
    }

    return (
        <div id="avatar-preview">
            <label htmlFor="avatar-loader">
                { img ? (
                    <img
                        src={ img }
                        alt={ t('profile.avatar') }
                    />
                ) : (
                    <div>{ t('system.upload') }</div>
                ) }

                <input
                    id="avatar-loader"
                    type="file"
                    accept="image/jpeg, image/png"
                    onChange={(_e) => { this.handleAvatar(_e) }}
                />
            </label>
        </div>
    )
}
