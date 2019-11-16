

import React from 'react';
import DeckGL from '@deck.gl/react';
import { LineLayer, ScatterplotLayer, PathLayer } from '@deck.gl/layers';
import { StaticMap } from 'react-map-gl';

// Set your mapbox access token here

const MAPBOX_ACCESS_TOKEN = "pk.eyJ1Ijoic2tlbGV0b3JraW5nIiwiYSI6ImNrMzE1cWFyYTA1OGczbnFqZ3pmYjI4cTEifQ.DjA1AD39dGKcW9kn94_hFQ";

// Initial viewport settings
const initialViewState = {
    latitude: 60.170,
    longitude: 24.9425964,
    zoom: 13,
    pitch: 0,
    bearing: 0,
    width: 50,
    height: 50
};

// Data to be used by the LineLayer
const data = [{ sourcePosition: [24.941, 60.169], targetPosition: [24.943, 60.172] }];
const scatterdata = [[24.943, 60.172]]
const pathdata = [{
    name: "random-name",
    color: [101, 147, 245],
    path: [[-74.00578, 40.713067],
    [-74.004577, 40.712425],
    [-74.003626, 40.713650],
    [-74.002666, 40.714243],
    [-74.002136, 40.715177],
    [-73.998493, 40.713452],
    [-73.997981, 40.713673],
    [-73.997586, 40.713448],
    [-73.99256, 40.713863]]
}
]

class FlowMap extends React.Component {

    render() {
        const layers = [
            new LineLayer({ id: 'line-layer', data }),
            new ScatterplotLayer({
                id: 'scatter-layer',
                radiusScale: 20,
                radiusMinPixels: 1.0,
                opacity: 0.8,
                data: scatterdata,
                getPosition: data => [data[0], data[1], 0],
                getColor: [0, 255, 255],
            }),
            new PathLayer({
                id: "path-layer",
                pathdata,
                getColor: data => data.color,
                widthMinPixels: 7
            })
        ];
        return (

            <DeckGL
                initialViewState={initialViewState}
                layers={layers}
                height="100%"
                width="50%"
                controller={false}
            >
                <StaticMap reuseMaps mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN} />
            </DeckGL>

        );
    }
}
export default FlowMap;

