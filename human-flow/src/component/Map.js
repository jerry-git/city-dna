/* global window */
import React, { Component } from 'react';
import { StaticMap } from 'react-map-gl';
import DeckGL from '@deck.gl/react';
import { ScatterplotLayer } from '@deck.gl/layers';
import { TripsLayer } from '@deck.gl/geo-layers';

import axios from "axios";
import moment from 'moment';

import "./Map.css";
// Set your mapbox token here

const MAPBOX_TOKEN = "pk.eyJ1Ijoic2tlbGV0b3JraW5nIiwiYSI6ImNrMzE1cWFyYTA1OGczbnFqZ3pmYjI4cTEifQ.DjA1AD39dGKcW9kn94_hFQ";

const start_time = "2019-08-11 22:00:00"
const end_time = "2019-08-12 05:00:00"



const DEFAULT_THEME = {
    trailColor0: [253, 128, 93],
    trailColor1: [23, 184, 190],
};

const INITIAL_VIEW_STATE = {
    longitude: 24.95,
    latitude: 60.17,
    zoom: 13,
    pitch: 40,
    bearing: 0
};

export class FlowMap extends Component {
    constructor(props) {
        super(props);
        this.state = {
            time: 0,
            drivedata: {},
            stationdata: {},
            start_of_animation: Date.now() / 1000,
            start_of_data: this._convert_time(start_time)

        };
    }

    componentDidMount() {
        axios({
            method: 'get',
            url: 'http://127.0.0.1:5000/stations',
            data: {
            }
        }).then((response) => {
            console.log(response);
            this.setState({ stationdata: response.data })
        }).catch(function (error) {
            console.log(error);
        });

        axios({
            method: 'post',
            url: 'http://127.0.0.1:5000/drives',
            data: {
                "start": start_time,
                "end": end_time
            }
        }).then((response) => {
            console.log(response);
            this.setState({ drivedata: response.data })
            this._animate();
        }).catch(function (error) {
            console.log(error);
        });


    }

    componentWillUnmount() {
        if (this._animationFrame) {
            window.cancelAnimationFrame(this._animationFrame);
        }
    }
    _convert_time(input) {
        var time = moment(input, 'YYYY-MM-DD hh:mm:ss');
        return time.format('X');
    }
    _utx_to_datetime(value) {
        return moment.unix(value).format("MM/DD/YYYY hh:mm:ss");
    }

    _animate() {
        const {
            animationSpeed = 220 // unit time per second
        } = this.props;

        const timer = (Date.now() / 1000) - this.state.start_of_animation;
        // console.log(this.state.time)

        this.setState({
            time: Math.floor((timer * animationSpeed))
        });

        this._animationFrame = window.requestAnimationFrame(this._animate.bind(this));
    }

    _renderWeather() {
        const {
            weather = [[24.931223405177413, 60.171870055373205], [24.94947287873, 60.1650171805]]
        } = this.props;

        return this.state.time;
    }

    _renderLayers() {
        const {
            trips = this.state.drivedata,

            trailLength = 80,
            theme = DEFAULT_THEME,

        } = this.props;

        return [
            new ScatterplotLayer({
                id: 'scatter-plot',
                data: this.state.stationdata,
                radiusScale: 10,
                radiusMinPixels: 0.5,
                getPosition: d => [d["lon"], d["lat"], 0],
                getColor: d => [255, 255, 0]
            }),

            new TripsLayer({
                id: 'trips',
                data: trips,
                getPath: d => d.path,
                getTimestamps: d => [this._convert_time(d.timestamps[0]) - this._convert_time(start_time), this._convert_time(d.timestamps[1]) - this._convert_time(start_time)],
                getColor: d => theme.trailColor0,
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
                <h1 class="center">{this._utx_to_datetime(Number(this.state.start_of_data) + this.state.time)}</h1>
                <div style={{ position: "relative" }}>
                    <DeckGL
                        layers={this._renderLayers()}
                        effects={theme.effects}
                        initialViewState={INITIAL_VIEW_STATE}
                        viewState={viewState}
                        controller={true}
                        width="100%"
                        height="900px"
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