import "cesium/Build/Cesium/Widgets/widgets.css";
import "./App.css";
import CesiumMap from "./components/CesiumMap";
import { JSX } from "react";

function App(): JSX.Element {
  return (
    <div className="App">
      <CesiumMap />
    </div>
  );
}

export default App;
