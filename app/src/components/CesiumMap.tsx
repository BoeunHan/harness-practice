import { useEffect, useRef, useState, forwardRef, useImperativeHandle } from "react";
import * as Cesium from "cesium";
import { useFreeFlightCamera } from "../hooks/useFreeFlightCamera";

export interface CesiumMapHandle {
  viewer: Cesium.Viewer | null;
}

const GANGNAM_LONGITUDE = 127.0276;
const GANGNAM_LATITUDE = 37.4979;
const INITIAL_HEIGHT = 40;

const CesiumMap = forwardRef<CesiumMapHandle>((_, ref) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const viewerRef = useRef<Cesium.Viewer | null>(null);
  const [viewer, setViewer] = useState<Cesium.Viewer | null>(null);

  useImperativeHandle(ref, () => ({
    get viewer() {
      return viewerRef.current;
    },
  }));

  useFreeFlightCamera(viewer);

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
        GANGNAM_LONGITUDE,
        GANGNAM_LATITUDE,
        INITIAL_HEIGHT,
      ),
      orientation: {
        heading: Cesium.Math.toRadians(45),
        pitch: Cesium.Math.toRadians(-15),
        roll: 0,
      },
    });

    viewerRef.current = cesiumViewer;
    setViewer(cesiumViewer);

    return () => {
      if (!cesiumViewer.isDestroyed()) {
        cesiumViewer.destroy();
      }
      viewerRef.current = null;
      setViewer(null);
    };
  }, []);

  return <div ref={containerRef} style={{ width: "100%", height: "100%" }} />;
});

CesiumMap.displayName = "CesiumMap";

export default CesiumMap;
