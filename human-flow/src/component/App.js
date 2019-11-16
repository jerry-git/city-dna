import React from "react";
import FlowMap from "./Map";
import TimeComponent from "./TimeComponent";

import "./App.css";

class App extends React.Component {
  render() {
    return (
      <div>
        <h1>Human Flow</h1>
        <div class="rowClass">
          <FlowMap />
        </div>
        {/* <TimeComponent /> */}
      </div>
    );
  }
}

export default App