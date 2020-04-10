import React from 'react'

import api from '../../func/api'

import CKEditor from '@ckeditor/ckeditor5-react'
import ClassicEditor from '@kosyachniy/ckeditor'

import './style.css'


export default class Editor extends React.Component {
	updatePost = (data) => {
		api('posts.edit', data)
	}

	handlerEditor = (event, editor) => {
		const data = {
			id: this.props.id,
			cont: editor.getData(),
		}

		this.updatePost(data)
	}

	render() {
		return (
			<CKEditor
				editor={ ClassicEditor }
				data={ this.props.cont }
				onChange={ this.handlerEditor }
			/>
		)
	}
}