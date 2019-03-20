import React from 'react'

import serverRequest from '../func/serverRequest'


export default class Main extends React.Component {
	state = {
		cont: 'Loading..',
	}

	componentWillMount() {
		const req = {
			'method': 'system.test',
			'language': 'ru',
		}

		serverRequest(req).then((res) => this.setState({cont: res['error']}))
	}

	render() {
		return (
			<div>
				{ this.state.cont }
			</div>
		)
	}
}