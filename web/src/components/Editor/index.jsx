import React from 'react'

import CKEditor from '@ckeditor/ckeditor5-react'
import ClassicEditor from '@kosyachniy/ckeditor'

import './style.css'


export default class Editor extends React.Component {
	render() {
		return (
			<CKEditor
				editor={ ClassicEditor }
				data={ this.props.cont }
				onChange={ (event, editor) => {this.props.updatePost(editor.getData())} }
			/>
		)
	}
}