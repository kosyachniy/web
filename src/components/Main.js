import React from 'react'

import getPost from '../func/methods'


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
			</div>
		)
	}
}