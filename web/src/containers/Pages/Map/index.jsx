import React from 'react'
// import { Link } from 'react-router-dom'

import { maps } from '../../../sets'
import Map from './Map'

// import './style.css'


export default class AllMap extends React.Component {
	constructor(props) {
		super(props)
	}

	// componentWillMount() {
	// 	this.setState({pet: document.location.search.split('&')[0].split('=').pop()});
	// }

	render() {
		return (
			<>
				<Map
					center={maps.center}
					zoom={maps.zoom}
					// current={this.state.currentLocation}
					// markers={this.state.markers}
					// handleOpen={this.handleOpen}
					// handleClose={this.handleClose}
				/>
			</>
		)
	}
}