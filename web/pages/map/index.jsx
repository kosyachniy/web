import Map from '../../components/Map'


export default () => {
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
