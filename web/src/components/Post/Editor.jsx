import React from 'react'

import { updatePost } from '../../func/methods'

import CKEditor from '@ckeditor/ckeditor5-react'
import ClassicEditor from '@ckeditor/ckeditor5-build-classic'


export default class Editor extends React.Component {
	// console.log(ClassicEditor.builtinPlugins.map( plugin => plugin.pluginName ))

	handlerEditor = (event, editor) => {
		const data = {
			id: this.props.id,
			cont: editor.getData(),
		}

		// console.log( {event, editor, data} )
	
		updatePost(this, data)
	}

	render() {
		return (
			<CKEditor
				editor={ ClassicEditor }
				config={ {
					// toolbar: ['bold', 'italic']
				} }

				data={ this.props.cont }

				onChange={ this.handlerEditor }
			/>
		)
	}
}