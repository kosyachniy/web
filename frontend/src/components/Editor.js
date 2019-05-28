import React from 'react'

import { updatePost } from '../func/methods'

import CKEditor from '@ckeditor/ckeditor5-react'
import ClassicEditor from '@ckeditor/ckeditor5-build-classic'


const handlerEditor = (event, editor) => {
	const data = editor.getData()
	// console.log( {event, editor, data} )

	updatePost(this, data)
}


export default class Editor extends React.Component {
	// console.log(ClassicEditor.builtinPlugins.map( plugin => plugin.pluginName ))

	render() {
		return (
			<CKEditor
				editor={ ClassicEditor }
				config={ {
					// toolbar: ['bold', 'italic']
				} }
				onChange={ handlerEditor }
			/>
		)
	}
}