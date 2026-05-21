import { useEffect, useRef, useState } from "react";
import * as Cesium from "cesium";
import { FirePosition } from "../types/fire";

const CENTER_LONGITUDE = 127.026177;
const CENTER_LATITUDE = 37.501197;
const RADIUS_METERS = 600;
const POOL_SIZE = 50;

function randomInRange(min: number, max: number): number {
  return Math.random() * (max - min) + min;
}

function randomOffsetDegrees(radiusMeters: number): {
  dLon: number;
  dLat: number;
} {
  const angle = Math.random() * 2 * Math.PI;
  const distance = Math.random() * radiusMeters;
  const dLat = (distance * Math.cos(angle)) / 111320;
  const dLon =
    (distance * Math.sin(angle)) /
    (111320 * Math.cos((CENTER_LATITUDE * Math.PI) / 180));
  return { dLon, dLat };
}

export function useFirePositionPool(viewer: Cesium.Viewer | undefined) {
  const [pool, setPool] = useState<FirePosition[]>([]);
  const [isReady, setIsReady] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (!viewer) return;

    let isCancelled = false;

    timerRef.current = setTimeout(async () => {
      const raycastTasks: {
        promise: Promise<any>;
        originalCoords: { longitude: number; latitude: number };
      }[] = [];

      for (let i = 0; i < POOL_SIZE; i++) {
        const { dLon, dLat } = randomOffsetDegrees(RADIUS_METERS);
        const lon = CENTER_LONGITUDE + dLon;
        const lat = CENTER_LATITUDE + dLat;
        const altitude = randomInRange(150, 250);

        const origin = Cesium.Cartesian3.fromDegrees(lon, lat, altitude);
        const { dLon: tDLon, dLat: tDLat } = randomOffsetDegrees(RADIUS_METERS);
        const target = Cesium.Cartesian3.fromDegrees(
          CENTER_LONGITUDE + tDLon,
          CENTER_LATITUDE + tDLat,
          0,
        );

        const direction = Cesium.Cartesian3.normalize(
          Cesium.Cartesian3.subtract(target, origin, new Cesium.Cartesian3()),
          new Cesium.Cartesian3(),
        );
        const ray = new Cesium.Ray(origin, direction);

        const unsafeScene = viewer.scene as any;
        raycastTasks.push({
          promise: unsafeScene.pickFromRayMostDetailed(ray),
          originalCoords: { longitude: lon, latitude: lat },
        });
      }

      const results = await Promise.all(
        raycastTasks.map((task) => task.promise),
      );

      if (isCancelled) return;

      const positions: FirePosition[] = [];

      for (let i = 0; i < results.length; i++) {
        const result = results[i];
        const { originalCoords } = raycastTasks[i];

        if (result && result.position) {
          const carto = Cesium.Cartographic.fromCartesian(result.position);
          positions.push({
            longitude: Cesium.Math.toDegrees(carto.longitude),
            latitude: Cesium.Math.toDegrees(carto.latitude),
            height: carto.height,
          });
        } else {
          positions.push({
            longitude: originalCoords.longitude,
            latitude: originalCoords.latitude,
            height: 0,
          });
        }
      }

      setPool(positions);
      setIsReady(true);
      timerRef.current = null;
    }, 1500);

    return () => {
      isCancelled = true;
      if (timerRef.current !== null) clearTimeout(timerRef.current);
    };
  }, [viewer]);

  return { FIRE_POSITIONS_POOL: pool, isReady };
}
