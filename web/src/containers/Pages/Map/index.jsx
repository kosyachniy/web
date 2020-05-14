import React from 'react'

import './style.css'
import Map from '../../../components/Map'


export default class WindowMap extends React.Component {
	// componentWillMount() {
	// 	this.setState({pet: document.location.search.split('&')[0].split('=').pop()});
	// }

	render() {
		return (
			<div id="map">
				<div>
					<Map />
				</div>
			</div>
		)
	}
}