import React from 'react'

import { getPost } from '../func/methods'

import Editor from './Editor'


export default class Main extends React.Component {
	state = {
		cont: 'Loading..',
	}

	componentWillMount() {
		getPost(this)
	}

	render() {
		return (
			<div>
				{ this.state.cont }
				<Editor />
			</div>
		)
	}
}