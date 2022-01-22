import _ from "lodash";
import React from 'react';
import { compose, withProps } from 'recompose';

// NOTE: "react-google-maps": "^9.4.5"
import { GoogleMap, Marker, withGoogleMap, withScriptjs } from 'react-google-maps'; // , InfoWindow
// import { Link } from 'react-router-dom';

import marker from './marker.svg';


class Maps extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            zoom: props.zoom ? props.zoom : process.env.REACT_APP_GOOGLE_MAPS_ZOOM,
            center: props.center ? props.center : {
                lat: process.env.REACT_APP_GOOGLE_MAPS_LAT,
                lng: process.env.REACT_APP_GOOGLE_MAPS_LNG,
            },
            current: props.center ? props.center : {
                lat: process.env.REACT_APP_GOOGLE_MAPS_LAT,
                lng: process.env.REACT_APP_GOOGLE_MAPS_LNG,
            },
            markers: [],
        }
    }

    componentWillMount() {
        if (!this.props.center) {
            if (window.navigator && window.navigator.geolocation) {
                window.navigator.geolocation.getCurrentPosition(
                    (pos) => {
                        const coords = pos.coords;
                        // console.log('My', coords);
                        this.setState({ current: { lat: coords.latitude, lng: coords.longitude }});
                    },
                    // (error) => {console.log(error)},
                    // { enableHighAccuracy: false, timeout: 200000, maximumAge: 1000 },
                );
            }
        }

        // getGeo(this);
    }

    // handleOpen = (id) => {
    //     let markers = this.state.markers
    //     markers[id].toggle = true
    //     this.setState({ markers })
    // }

    // handleClose = (id) => {
    //     let markers = this.state.markers
    //     markers[id].toggle = false
    //     this.setState({ markers })
    // }

    // handleFavorite = (id) => {
    //     let markers = this.state.markers;

    //     if (markers[id].donor.way) {
    //         delWay(this, {
    //             id: markers[id].donor.way,
    //         }).then(res => {
    //             markers[id].donor.way = 0;
    //             this.setState({ markers });
    //         })

    //         this.setState({ markers })
    //     } else {
    //         addWay(this, {
    //             type: 1,
    //             cont: markers[id].donor.id,
    //         }).then(res => {
    //             markers[id].donor.way = res;
    //             this.setState({ markers });
    //         })
    //     }
    // }

    render() {
        return (
            <GoogleMap
                defaultZoom={this.state.zoom}
                defaultCenter={this.state.center}
                options={{ streetViewControl: false, mapTypeControl: false, gestureHandling: 'greedy', styles: mapStyles }}
            >
                <Marker
                    icon={{
                        url: marker,
                        scaledSize: new window.google.maps.Size(40, 40)
                    }}
                    position={ this.state.current }
                    key="i"
                />
                {/* {this.state.markers.map((el, key) => (
                    <Marker
                        position={ el.geo }
                        key={ key }
                        onClick={ () => {this.handleOpen(key)} }
                    >
                        { el.toggle && (
                            <InfoWindow
                                // options={{
                                //     pane: "overlayLayer",
                                //     alignBottom: true,
                                //     boxStyle: {
                                //         boxShadow: `3px 3px 10px rgba(0,0,0,0)`
                                //     },
                                // }}
                                // onCloseClick={ () => {this.handleClose(key)} } style={{ padding: 0, margin: 0 }}
                            >
                                <div className="info-window">
                                    <div className="first-line">
                                        <div>
                                            <i className="bi bi-compass-fill" style={{ fontSize: '1.2rem', cursor: 'pointer', color: el.donor.way ? 'red' : '#6c757d' }} onClick={ () => { this.handleFavorite(key) } } />
                                        </div>
                                        <div>
                                            <i className="bi bi-share-fill" style={{ fontSize: '1.2rem', cursor: 'pointer' }} />
                                            &nbsp;
                                            <i className="bi bi-x" style={{ fontSize: '1.2rem', cursor: 'pointer' }} onClick={ () => {this.handleClose(key)} } />
                                        </div>
                                    </div>
                                    <table>
                                        <tbody>
                                            <tr>
                                                <td>{ el.donor.name }</td>
                                                <td>Звонить с { el.donor.from } до { el.donor.to }</td>
                                            </tr>
                                            <tr>
                                                <td>Порода:</td>
                                                <td>{ el.donor.breed } ({ el.donor.type === 1 ? 'кот' : 'собака' })</td>
                                            </tr>
                                            <tr>
                                                <td>Прививки:</td>
                                                <td>{ el.donor.vaccinations ? 'да' : 'нет' }</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <div className="third-line">
                                        <Link to="">Подробнее</Link>
                                    </div>
                                    <div className="last-line">
                                        <a href={ "tel:+" + el.donor.phone }><div>Позвонить</div></a>
                                        <a href={ "sms:+" + el.donor.phone }><div>Написать</div></a>
                                    </div>
                                </div>
                            </InfoWindow>
                        )}
                    </Marker>
                ))} */}
            </GoogleMap>
        )
    }
}


const mapStyles = [
    {
        elementType: 'labels.icon',
        stylers: [
            {
                visibility: 'off',
            },
        ],
    },
];

const Map = compose(
    withProps({
        googleMapURL: `https://maps.googleapis.com/maps/api/js?key=${process.env.REACT_APP_GOOGLE_MAPS_KEY}&v=3.exp&libraries=geometry,drawing,places`,
        loadingElement: <div style={{ height: `100%` }} />,
        containerElement: <div style={{ height: `100%` }} />,
        mapElement: <div style={{ height: `100%` }} />
    }),
    withScriptjs,
    withGoogleMap
)((props) => (
    <Maps
        center={props.center}
        zoom={props.zoom}
    />
));


const enhance = _.identity;
export default enhance(Map);
