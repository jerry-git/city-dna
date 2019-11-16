import React, { Component } from 'react';

class TimeComponent extends Component {
    constructor(props) {
        super(props);
        this.state = { time: Date.now() };
    }
    render() {
        return (
            <div> {this.state.time} </div>
        );
    }

    componentDidMount() {
        this.interval = setInterval(() => this.setState({ time: Date.now() }), 1000);
    }
    componentWillUnmount() {
        clearInterval(this.interval);
    }
}

export default TimeComponent;