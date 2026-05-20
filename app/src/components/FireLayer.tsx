import { useEffect, useRef } from "react";
import * as Cesium from "cesium";
import { FireEvent } from "../types/fire";

interface FireLayerProps {
  fires: FireEvent[];
  extinguish: (id: string) => void;
  viewer: Cesium.Viewer;
}

export default function FireLayer({
  fires,
  extinguish,
  viewer,
}: FireLayerProps) {
  const handlerRef = useRef<Cesium.ScreenSpaceEventHandler | null>(null);

  useEffect(() => {
    if (!viewer) return;

    viewer.entities.removeAll();

    fires.forEach((fire) => {
      const { id, longitude, latitude, height, fireSize, smokeHeight } = fire;

      viewer.entities.add({
        id: `${id}_smoke`,
        position: Cesium.Cartesian3.fromDegrees(
          longitude,
          latitude,
          height + smokeHeight / 2,
        ),
        allowPicking: false,
        cylinder: {
          length: smokeHeight,
          topRadius: smokeHeight * 0.3,
          bottomRadius: 1,
          material: Cesium.Color.GRAY.withAlpha(0.4),
        },
      } as any);

      viewer.entities.add({
        id: `${id}_fire`,
        position: Cesium.Cartesian3.fromDegrees(
          longitude,
          latitude,
          height + fireSize / 2,
        ),
        cylinder: {
          length: fireSize,
          topRadius: fireSize * 0.5,
          bottomRadius: fireSize * 0.5,
          material: Cesium.Color.RED.withAlpha(0.9),
        },
      });
    });
  }, [fires, viewer]);

  useEffect(() => {
    if (!viewer) return;

    const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
    handlerRef.current = handler;

    handler.setInputAction(
      (movement: Cesium.ScreenSpaceEventHandler.PositionedEvent) => {
        const picked = viewer.scene.pick(movement.position);
        if (Cesium.defined(picked) && picked.id instanceof Cesium.Entity) {
          const entityId: string = picked.id.id;
          // 연기 엔티티(_smoke) 클릭은 무시하고 불 엔티티(_fire)만 처리
          if (entityId.endsWith("_fire")) {
            const fireId = entityId.slice(0, -5);
            extinguish(fireId);
          }
        }
      },
      Cesium.ScreenSpaceEventType.LEFT_CLICK,
    );

    return () => {
      handler.destroy();
      handlerRef.current = null;
    };
  }, [viewer, extinguish]);

  useEffect(() => {
    return () => {
      if (viewer && !viewer.isDestroyed()) {
        viewer.entities.removeAll();
      }
    };
  }, [viewer]);

  return null;
}
