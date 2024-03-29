/* global window */
import React, { Component } from 'react';

import Switch from "react-switch";
import { StaticMap } from 'react-map-gl';
import DeckGL from '@deck.gl/react';
import { ScatterplotLayer } from '@deck.gl/layers';
import { TripsLayer } from '@deck.gl/geo-layers';

import axios from "axios";
import moment from 'moment';

import "./Map.css";
// Set your mapbox token here

const MAPBOX_TOKEN = "pk.eyJ1Ijoic2tlbGV0b3JraW5nIiwiYSI6ImNrMzE1cWFyYTA1OGczbnFqZ3pmYjI4cTEifQ.DjA1AD39dGKcW9kn94_hFQ";

const start_time = "2019-09-06 06:00:00"
const end_time = "2019-09-06 23:00:00"



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
            predicted_drive_data: {},
            stationdata: {},
            weatherdata: {},
            weather_info_text: "",
            start_of_animation: Date.now() / 1000,
            start_of_data: this._convert_time(start_time),
            show_prediction: true

        };

        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(checked) {
        this.setState({ checked });
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
            method: 'get',
            url: 'http://127.0.0.1:5000/weather',
            data: {
            }
        }).then((response) => {
            console.log(response);
            this.setState({ weatherdata: response.data })
        }).catch(function (error) {
            console.log(error);
        });
        axios({
            method: 'post',
            url: 'http://127.0.0.1:5000/drives?predicted=1',
            data: {
                "start": start_time,
                "end": end_time
            }
        }).then((response) => {
            console.log(response);
            this.setState({ predicted_drive_data: response.data })
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
        return moment.unix(value).format("dddd DD-MM-YYYY kk:mm");
    }

    _animate() {
        const {
            animationSpeed = 220 // unit time per second
        } = this.props;

        const timer = (Date.now() / 1000) - this.state.start_of_animation;

        this.setState({
            time: Math.floor((timer * animationSpeed))
        });
        var index = Number(this.state.start_of_data) + this.state.time - Number(this._convert_time(this.state.weatherdata[1].time))
        index = Math.floor(index/3600) +1
        this.setState({
            weather_info_text: "Temp: " + this.state.weatherdata[index].temp + " C, " + " Clouds: " + this.state.weatherdata[index].clouds +"/8, Rain: " + this.state.weatherdata[index].rain +"mm/h"
        });


        this._animationFrame = window.requestAnimationFrame(this._animate.bind(this));
    }


    _renderLayers() {
        const {
            trips = this.state.drivedata,
            predicted_trips = this.state.predicted_drive_data,
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
                getColor: d => theme.trailColor1,
                opacity: 0.3,
                widthMinPixels: 5,
                rounded: true,
                trailLength,
                currentTime: this.state.time,
                shadowEnabled: false
            }),
            new TripsLayer({
                id: 'trips2',
                data: predicted_trips,
                getPath: d => d.path,
                getTimestamps: d => [this._convert_time(d.timestamps[0]) - this._convert_time(start_time), this._convert_time(d.timestamps[1]) - this._convert_time(start_time)],
                getColor: d => theme.trailColor0,
                opacity: 0.3,
                widthMinPixels: 5,
                rounded: true,
                trailLength,
                currentTime: this.state.time,
                shadowEnabled: false,
                visible:this.state.checked
            })
        ];
    }

    render() {
        const {
            viewState,
            mapStyle = 'mapbox://styles/mapbox/dark-v10',
            theme = DEFAULT_THEME
            
        } = this.props;


        return (
            <React.Fragment>
                <div>
                    <h2 className="center">{this._utx_to_datetime(Number(this.state.start_of_data) + this.state.time) }</h2>
                    <h2 className="center">{this.state.weather_info_text}</h2>
                    <div className="toggle">
                        <Switch onChange={this.handleChange} checked={this.state.checked} uncheckedIcon={false} checkedIcon={false}/>
                    </div>
                    <div className="toggle2">
                        <h3 className="center" >Prediction</h3>
                    </div>
                </div>
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