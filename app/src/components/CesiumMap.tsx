import { useEffect, useRef, forwardRef, useImperativeHandle } from "react";
import * as Cesium from "cesium";

export interface CesiumMapHandle {
  viewer: Cesium.Viewer | null;
}

const GANGNAM_LONGITUDE = 127.0276;
const GANGNAM_LATITUDE = 37.4979;
const INITIAL_HEIGHT = 40;

const CesiumMap = forwardRef<CesiumMapHandle>((_, ref) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const viewerRef = useRef<Cesium.Viewer | null>(null);

  useImperativeHandle(ref, () => ({
    get viewer() {
      return viewerRef.current;
    },
  }));

  useEffect(() => {
    if (!containerRef.current) return;

    const token = import.meta.env.VITE_CESIUM_TOKEN;
    Cesium.Ion.defaultAccessToken = token;

    const viewer = new Cesium.Viewer(containerRef.current, {
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
    viewer.scene.globe.depthTestAgainstTerrain = true;

    // 지형 입체화
    Cesium.createWorldTerrainAsync().then((terrainProvider) => {
      viewer.terrainProvider = terrainProvider;
    });

    // 건물 입체화
    Cesium.createOsmBuildingsAsync().then((osmBuildings) => {
      viewer.scene.primitives.add(osmBuildings);
    });

    viewer.camera.setView({
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

    viewerRef.current = viewer;

    return () => {
      if (!viewer.isDestroyed()) {
        viewer.destroy();
      }
      viewerRef.current = null;
    };
  }, []);

  return <div ref={containerRef} style={{ width: "100%", height: "100%" }} />;
});

CesiumMap.displayName = "CesiumMap";

export default CesiumMap;
