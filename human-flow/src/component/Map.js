/* global window */
import React, { Component } from 'react';
import { StaticMap } from 'react-map-gl';
import DeckGL from '@deck.gl/react';
import { PolygonLayer, ScatterplotLayer } from '@deck.gl/layers';
import { TripsLayer } from '@deck.gl/geo-layers';

import "./Map.css";
// Set your mapbox token here

const MAPBOX_TOKEN = "pk.eyJ1Ijoic2tlbGV0b3JraW5nIiwiYSI6ImNrMzE1cWFyYTA1OGczbnFqZ3pmYjI4cTEifQ.DjA1AD39dGKcW9kn94_hFQ";

// Source data CSV
const DATA_URL = {
    TRIPS:
        'https://raw.githubusercontent.com/uber-common/deck.gl-data/master/examples/trips/trips-v7.json' // eslint-disable-line
};


const DEFAULT_THEME = {
    trailColor0: [253, 128, 93],
    trailColor1: [23, 184, 190],
};

const INITIAL_VIEW_STATE = {
    longitude: 24.91,
    latitude: 60.17,
    zoom: 13,
    pitch: 45,
    bearing: 0
};

const landCover = [[[60.17, 24.91], [60.19, 24.91], [60.19, 24.93], [60.17, 24.93]]];

export class FlowMap extends Component {
    constructor(props) {
        super(props);
        this.state = {
            time: 0
        };
    }

    componentDidMount() {
        this._animate();
    }

    componentWillUnmount() {
        if (this._animationFrame) {
            window.cancelAnimationFrame(this._animationFrame);
        }
    }

    _animate() {
        const {
            loopLength = 1800, // unit corresponds to the timestamp in source data
            animationSpeed = 30 // unit time per second
        } = this.props;
        const timestamp = Date.now() / 1000;
        const loopTime = loopLength / animationSpeed;

        this.setState({
            time: ((timestamp % loopTime) / loopTime) * loopLength
        });
        this._animationFrame = window.requestAnimationFrame(this._animate.bind(this));
    }

    _renderLayers() {
        const {
            trips = DATA_URL.TRIPS,
            trailLength = 180,
            theme = DEFAULT_THEME,
            stationdata = [[24.931223405177413, 60.171870055373205], [24.94947287873, 60.1650171805]]
        } = this.props;

        return [
            new ScatterplotLayer({
                id: 'scatter-plot',
                data: stationdata,
                radiusScale: 20,
                radiusMinPixels: 0.5,
                getPosition: d => [d[0], d[1], 0],
                getColor: d => [255, 255, 0]
            }),
            // This is only needed when using shadow effects
            new PolygonLayer({
                id: 'ground',
                data: landCover,
                getPolygon: f => f,
                stroked: false,
                getFillColor: [0, 0, 0, 0]
            }),
            new TripsLayer({
                id: 'trips',
                data: trips,
                getPath: d => d.path,
                getTimestamps: d => d.timestamps,
                getColor: d => (d.vendor === 0 ? theme.trailColor0 : theme.trailColor1),
                opacity: 0.3,
                widthMinPixels: 2,
                rounded: true,
                trailLength,
                currentTime: this.state.time,

                shadowEnabled: false
            }),
        ];
    }

    render() {
        const {
            viewState,
            mapStyle = 'mapbox://styles/mapbox/dark-v9',
            theme = DEFAULT_THEME
        } = this.props;

        return (
            <React.Fragment>
                <h1 class="center">{this.state.time}</h1>
                <div class="center" style={{ position: "relative" }}>
                    <DeckGL
                        layers={this._renderLayers()}
                        effects={theme.effects}
                        initialViewState={INITIAL_VIEW_STATE}
                        viewState={viewState}
                        controller={true}
                        width="100%"
                        height="800px"
                    >
                        <StaticMap
                            reuseMaps
                            mapStyle={mapStyle}
                            preventStyleDiffing={true}
                            mapboxApiAccessToken={MAPBOX_TOKEN}
                        />
                    </DeckGL>
                </div>

            </React.Fragment>
        );
    }
}

export default FlowMap