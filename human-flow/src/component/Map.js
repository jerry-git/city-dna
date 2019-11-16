import "mapbox-gl/dist/mapbox-gl.css";
import React, { Component } from "react";
import MapGL from "react-map-gl";
import DeckGL from '@deck.gl/layers';


// Please be a decent human and don't abuse my Mapbox API token.
// Ways to set Mapbox token: https://uber.github.io/react-map-gl/#/Documentation/getting-started/about-mapbox-tokens
const MAPBOX_TOKEN =
    "pk.eyJ1Ijoic21peWFrYXdhIiwiYSI6ImNqcGM0d3U4bTB6dWwzcW04ZHRsbHl0ZWoifQ.X9cvdajtPbs9JDMG-CMDsA";

class Map extends Component {
    state = {
        viewport: {
            width: 200,
            height: 400,
            latitude: 60.17,
            longitude: 24.9425964,
            zoom: 13.5
        },
        searchResultLayer: null
    };

    mapRef = React.createRef();

    componentDidMount() {
        window.addEventListener("resize", this.resize);
        this.resize();
    }

    componentWillUnmount() {
        window.removeEventListener("resize", this.resize);
    }

    resize = () => {
        this.handleViewportChange({
            width: window.innerWidth,
            height: window.innerHeight
        });
    };

    handleViewportChange = viewport => {
        this.setState({
            viewport: { ...this.state.viewport, ...viewport }
        });
    };



    render() {
        const { viewport } = this.state;

        return (
            <MapGL
                ref={this.mapRef}
                {...viewport}
                onViewportChange={this.handleViewportChange}
                mapboxApiAccessToken={MAPBOX_TOKEN}
            >
            </MapGL>
        );
    }
}

export default Map; 
