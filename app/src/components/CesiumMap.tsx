import { useEffect, useRef, forwardRef, useImperativeHandle } from "react";
import * as Cesium from "cesium";

export interface CesiumMapHandle {
  viewer: Cesium.Viewer | null;
}

const GANGNAM_LONGITUDE = 127.0276;
const GANGNAM_LATITUDE = 37.4979;
const INITIAL_HEIGHT = 500;

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

    const viewer = new Cesium.Viewer(containerRef.current, {
      timeline: false,
      animation: false,
      baseLayerPicker: false,
      geocoder: false,
      homeButton: true,
      sceneModePicker: false,
      navigationHelpButton: false,

      baseLayer: Cesium.ImageryLayer.fromProviderAsync(
        Cesium.IonImageryProvider.fromAssetId(2, {
          accessToken: token,
        }),
      ),
    });

    viewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(
        GANGNAM_LONGITUDE,
        GANGNAM_LATITUDE,
        INITIAL_HEIGHT,
      ),
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
