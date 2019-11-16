import React from "react";
import Map from "./Map";

import "./App.css";

class App extends React.Component {
  state = {
    total: null,
    next: null,
    operation: null,
  };


  render() {
    return (
      <div>
        <Map />
      </div>
    );
  }
}

export default App