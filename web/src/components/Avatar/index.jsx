import React from 'react'

import './style.css'


export default class Avatar extends React.Component {
	state = {
		img: null, // this.props.avatar,
	}

	handleAvatar = (_e) => {
		const cover = _e.target.files
		const fileReader = new FileReader()

		fileReader.onload = (_eventFileReader) => {
			const base64 = _eventFileReader.target.result
			const avatar = base64.split(',')[1]
			const file = cover[0].name

			this.setState({ img: base64 })
			this.props.updateAvatar(avatar, file)
		}
		fileReader.readAsDataURL(cover[0])
	}

	render() {
		return (
			<div id="avatar-preview">
				<label htmlFor="avatar-loader">
					{ this.state.img ? (
						<img src={ this.state.img } alt={ 'аватарка' } />
					) : (
						<div>Загрузите фото</div>
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