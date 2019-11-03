import React from 'react'

import { updatePost } from '../../func/methods'

import CKEditor from '@ckeditor/ckeditor5-react'
import ClassicEditor from '@kosyachniy/ckeditor'

import './style.css'


export default class Editor extends React.Component {
	handlerEditor = (event, editor) => {
		const data = {
			id: this.props.id,
			cont: editor.getData(),
		}

		updatePost(this, data)
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