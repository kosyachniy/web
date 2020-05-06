import React, { useState } from 'react'
import { Redirect } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

import api from '../../../func/api'

import Editor from '../../../components/Editor'


const Edit = (props) => {
	const [state, setState] = useState({
		name: props.post ? props.post.name : '',
		cont: props.post ? props.post.cont : '',
		redirect: null,
	})

	const { t } = useTranslation()

	const editPost = () => {
		let data = {
			name: state.name,
			cont: state.cont,
		}

		if (props.post) {
			data['id'] = props.post.id
		}

		const handlerSuccess = res => {
			if (props.post) {
				props.handlerSave()
			} else {
				setState({ ...state, redirect: res.id })
			}
		}

		api('posts.edit', data, handlerSuccess)
	}

	if (state.redirect) {
		return (
			<Redirect to={`/post/${state.redirect}`} />
		)
	}

	return (
		<div id="edit">
			<div className="album py-5">
				<div className="form-group">
					<input
						type="text"
						className="form-control"
						placeholder={ t('posts.name') }
						value={ state.name }
						onChange={ (event) => {setState({ ...state, name: event.target.value })} }
					/>
				</div>

				<Editor
					cont={ state.cont }
					updatePost={ (cont) => {setState({ ...state, cont })} }
				/>

				<br />
				<button
					className="btn btn-success"
					style={ {width: '100%'} }
					onClick={ editPost }
				>
					<i className="far fa-save" />
				</button>
			</div>
		</div>
	);
};

export default Edit;