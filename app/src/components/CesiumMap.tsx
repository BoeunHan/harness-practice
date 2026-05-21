import { useEffect, useRef, useState } from "react";
import * as Cesium from "cesium";
import { useFreeFlightCamera } from "../hooks/useFreeFlightCamera";
import { useFirePositionPool } from "../hooks/useFirePositionPool";
import { useFireSimulation } from "../hooks/useFireSimulation";
import FireLayer from "./FireLayer";
import FireDashboard from "./FireDashboard";
import FpsOverlay from "./FpsOverlay";

const FIRE_CENTER_LONGITUDE = 127.026177;
const FIRE_CENTER_LATITUDE = 37.501197;
const INITIAL_HEIGHT = 100;

export default function CesiumMap() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [viewer, setViewer] = useState<Cesium.Viewer | null>(null);

  const { isLocked } = useFreeFlightCamera(viewer);

  const handleRequestLock = () => {
    viewer?.canvas.requestPointerLock();
  };

  const { FIRE_POSITIONS_POOL, isReady } = useFirePositionPool(
    viewer ?? undefined,
  );
  const { fires, extinguish } = useFireSimulation({
    firePositionPool: FIRE_POSITIONS_POOL,
    isPoolReady: isReady,
  });

  useEffect(() => {
    if (!containerRef.current) return;

    const token = import.meta.env.VITE_CESIUM_TOKEN;
    Cesium.Ion.defaultAccessToken = token;

    const cesiumViewer = new Cesium.Viewer(containerRef.current, {
      timeline: false,
      animation: false,
      baseLayerPicker: false,
      geocoder: false,
      homeButton: true,
      sceneModePicker: false,
      navigationHelpButton: false,

      baseLayer: Cesium.ImageryLayer.fromProviderAsync(
        Cesium.IonImageryProvider.fromAssetId(2),
      ),
    });

    // 지형과 건물의 깊이 테스트 활성화
    cesiumViewer.scene.globe.depthTestAgainstTerrain = true;

    // 지형 입체화
    Cesium.createWorldTerrainAsync().then((terrainProvider) => {
      cesiumViewer.terrainProvider = terrainProvider;
    });

    // 건물 입체화
    Cesium.createOsmBuildingsAsync().then((osmBuildings) => {
      cesiumViewer.scene.primitives.add(osmBuildings);
    });

    cesiumViewer.camera.setView({
      destination: Cesium.Cartesian3.fromDegrees(
        FIRE_CENTER_LONGITUDE,
        FIRE_CENTER_LATITUDE,
        INITIAL_HEIGHT,
      ),
      orientation: {
        heading: Cesium.Math.toRadians(45),
        pitch: Cesium.Math.toRadians(-15),
        roll: 0,
      },
    });

    setViewer(cesiumViewer);

    return () => {
      if (!cesiumViewer.isDestroyed()) {
        cesiumViewer.destroy();
      }
      setViewer(null);
    };
  }, []);

  return (
    <>
      <div ref={containerRef} style={{ width: "100%", height: "100%" }} />
      {viewer && (
        <FireLayer fires={fires} extinguish={extinguish} viewer={viewer} />
      )}
      <FireDashboard count={fires.length} />
      <FpsOverlay isLocked={isLocked} onRequestLock={handleRequestLock} />
    </>
  );
}
