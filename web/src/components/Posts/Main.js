import React from 'react'

import { getPost } from '../../func/methods'

import Post from './Post'
import Editor from './Editor'


export default class Main extends React.Component {
	state = {
		posts: [],
	}

	componentWillMount() {
		getPost(this)
	}

	render() {
		return (
			<div class="album py-5 bg-light">
				<div class="container">
					<div class="row">
						{ this.state.posts.map((el, num) => 
							<Post key={ num } el={ el } />
						) }
						{/* <Editor /> */}
					</div>
				</div>
			</div>
		)
	}
}