import { useEffect, useRef } from "react";
import * as Cesium from "cesium";
import { FireEvent } from "../types/fire";

interface FireLayerProps {
  fires: FireEvent[];
  extinguish: (id: string) => void;
  viewer: Cesium.Viewer;
  isLocked: boolean;
}

const MAX_INTERACTION_DISTANCE = 150;

export default function FireLayer({
  fires,
  extinguish,
  viewer,
  isLocked,
}: FireLayerProps) {
  const prevEntityIdsRef = useRef<Set<string>>(new Set());

  useEffect(() => {
    if (!viewer) return;

    const currentEntityIds = new Set<string>();

    fires.forEach((fire) => {
      const { id, longitude, latitude, height, fireSize, smokeHeight } = fire;
      const smokeId = `${id}_smoke`;
      const fireId = `${id}_fire`;

      currentEntityIds.add(smokeId);
      currentEntityIds.add(fireId);

      let smokeEntity = viewer.entities.getById(smokeId);
      const smokePosition = Cesium.Cartesian3.fromDegrees(
        longitude,
        latitude,
        height + smokeHeight / 2,
      );

      if (!smokeEntity) {
        // 없을 때만 최초 1회 생성
        viewer.entities.add({
          id: smokeId,
          position: smokePosition as any,
          allowPicking: false,
          cylinder: {
            length: smokeHeight,
            topRadius: smokeHeight * 0.3,
            bottomRadius: 1,
            material: Cesium.Color.GRAY.withAlpha(0.4),
          },
        } as any);
      } else {
        // 이미 있으면 성능 저하 없이 위치와 크기 값만 실시간 업데이트
        smokeEntity.position = smokePosition as any;
        if (smokeEntity.cylinder) {
          smokeEntity.cylinder.length = smokeHeight as any;
          smokeEntity.cylinder.topRadius = (smokeHeight * 0.3) as any;
        }
      }

      let fireEntity = viewer.entities.getById(fireId);
      const firePosition = Cesium.Cartesian3.fromDegrees(
        longitude,
        latitude,
        height + fireSize / 2,
      );

      if (!fireEntity) {
        // 없을 때만 최초 1회 생성
        viewer.entities.add({
          id: fireId,
          position: firePosition as any,
          cylinder: {
            length: fireSize,
            topRadius: fireSize * 0.5,
            bottomRadius: fireSize * 0.5,
            material: Cesium.Color.RED.withAlpha(0.9),
          },
        });
      } else {
        // 이미 있으면 위치와 크기 값만 업데이트
        fireEntity.position = firePosition as any;
        if (fireEntity.cylinder) {
          fireEntity.cylinder.length = fireSize as any;
          fireEntity.cylinder.topRadius = (fireSize * 0.5) as any;
          fireEntity.cylinder.bottomRadius = (fireSize * 0.5) as any;
        }
      }
    });

    // 리스트에서 사라진(진화된) 엔티티만 골라서 제거
    prevEntityIdsRef.current.forEach((prevId) => {
      if (!currentEntityIds.has(prevId)) {
        viewer.entities.removeById(prevId);
      }
    });

    prevEntityIdsRef.current = currentEntityIds;
  }, [fires, viewer]);

  useEffect(() => {
    if (!viewer) return;

    const handleClick = () => {
      if (!isLocked) return;

      const centerX = viewer.canvas.clientWidth / 2;
      const centerY = viewer.canvas.clientHeight / 2;
      const picked = viewer.scene.pick(new Cesium.Cartesian2(centerX, centerY));

      if (Cesium.defined(picked) && picked.id instanceof Cesium.Entity) {
        const entityId: string = picked.id.id;
        // 연기 엔티티(_smoke) 클릭은 무시하고 불 엔티티(_fire)만 처리
        if (entityId.endsWith("_fire")) {
          const fireId = entityId.slice(0, -5);
          const entity = picked.id;

          if (entity.position) {
            const cameraPosition = viewer.camera.position;
            let entityPosition: Cesium.Cartesian3;

            // position이 CallbackProperty인 경우 평가
            if (typeof entity.position.getValue === "function") {
              entityPosition = entity.position.getValue(
                Cesium.JulianDate.now(),
              );
            } else {
              entityPosition = entity.position as Cesium.Cartesian3;
            }

            const distance = Cesium.Cartesian3.distance(
              cameraPosition,
              entityPosition,
            );

            if (distance <= MAX_INTERACTION_DISTANCE) {
              extinguish(fireId);
            }
          }
        }
      }
    };

    document.addEventListener("click", handleClick);

    return () => {
      document.removeEventListener("click", handleClick);
    };
  }, [viewer, extinguish, isLocked]);

  useEffect(() => {
    return () => {
      if (viewer && !viewer.isDestroyed()) {
        viewer.entities.removeAll();
      }
    };
  }, [viewer]);

  return null;
}
