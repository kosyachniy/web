import Map from '../../../components/Map'

import './style.css'


const WindowMap = () => {
    // componentWillMount() {
    //     this.setState({pet: document.location.search.split('&')[0].split('=').pop()});
    // }

    return (
        <div id="map">
            <div>
                <Map />
            </div>
        </div>
    )
}

export default WindowMap;
