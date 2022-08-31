import React from 'react'
import { useTranslation } from 'next-i18next';

import uploadImage from '../functions/upload'

import './style.css'


class Avatar extends React.Component {
    state = {
        img: this.props.avatar,
    }

    handleAvatar = (_e) => {
        const image = _e.target.files[0]
        uploadImage(image).then((link) => {
            this.setState({ img: link })
            this.props.setAvatar(link)
        })
    }

    render() {
        const { t } = useTranslation('common')

        return (
            <div id="avatar-preview">
                <label htmlFor="avatar-loader">
                    { this.state.img ? (
                        <img
                            src={ this.state.img }
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
}

export default withTranslation()(Avatar);