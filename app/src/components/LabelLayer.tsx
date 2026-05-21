import { useEffect, useRef } from "react";
import * as Cesium from "cesium";
import { Label } from "../types/label";
import { createHighDPICircleMarker } from "../utils/markerCanvas";

interface LabelLayerProps {
  labels: Label[];
  viewer: Cesium.Viewer;
}

export default function LabelLayer({ labels, viewer }: LabelLayerProps) {
  const entityIdsRef = useRef<Set<string>>(new Set());

  useEffect(() => {
    if (!viewer) return;

    const currentEntityIds = new Set<string>();

    labels.forEach((label) => {
      currentEntityIds.add(label.id);

      let entity = viewer.entities.getById(label.id);

      const cartographic = Cesium.Cartographic.fromDegrees(
        label.longitude,
        label.latitude,
      );

      const height = viewer.scene.sampleHeight(cartographic) ?? 0;
      const finalHeight = label.height ?? height + 100;

      if (!entity) {
        const position = Cesium.Cartesian3.fromDegrees(
          label.longitude,
          label.latitude,
          finalHeight,
        );

        // 정교하고 해상도 높은 Canvas 마커를 생성 (글자까지 한 번에 구워냄)
        const markerCanvas = createHighDPICircleMarker(
          label.name,
          label.borderColor,
          6,
        );

        viewer.entities.add({
          id: label.id,
          position: position,
          billboard: {
            image: markerCanvas as any,
            horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
            verticalOrigin: Cesium.VerticalOrigin.CENTER,

            // 깨짐 방지의 핵심: 픽셀을 강제로 늘리는 대신, 원래 크기(1.0)를 최대치로 잡고 멀어지면 줄어들게 처리
            // Near가 100m일 때 1.0배 (가장 선명함), Far가 2000m일 때 0.4배로 축소
            scaleByDistance: new Cesium.NearFarScalar(100, 1.0, 2000, 0.4),

            // 건물이나 지형에 가려져도 글자가 뚫고 보이게 하려면 무한대 설정 (선택 사항)
            disableDepthTestDistance: Number.POSITIVE_INFINITY,
          },
        });
      }
    });

    entityIdsRef.current.forEach((prevId) => {
      if (!currentEntityIds.has(prevId)) {
        viewer.entities.removeById(prevId);
      }
    });

    entityIdsRef.current = currentEntityIds;
  }, [labels, viewer]);

  return null;
}
