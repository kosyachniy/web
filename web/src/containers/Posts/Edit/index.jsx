import React, { useState } from 'react'
import { Redirect } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

import api from '../../../func/api'

import './style.css'
import Editor from '../../../components/Editor'


const Edit = (props) => {
	const [name, setName] = useState(props.post ? props.post.name : '')
	const [cont, setCont] = useState(props.post ? props.post.cont : '')
	const [redirect, setRedirect] = useState(null)
	const { t } = useTranslation()

	const editPost = () => {
		let data = { name, cont }

		if (props.post) {
			data['id'] = props.post.id
		}

		const handlerSuccess = res => {
			if (props.post) {
				props.handlerSave()
			} else {
				setRedirect(res.id)
			}
		}

		api('posts.edit', data, handlerSuccess)
	}

	if (redirect) {
		return (
			<Redirect to={`/post/${redirect}`} />
		)
	}

	return (
		<div id="edit">
			<div className="album py-5">
				<div className="form-group">
					<input
						type="text"
						className="form-control name"
						placeholder={ t('posts.name') }
						value={ name }
						onChange={ (event) => {setName(event.target.value)} }
					/>
				</div>

				<Editor
					cont={ cont }
					updatePost={ (text) => {setCont(text)} }
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