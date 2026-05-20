import { useEffect } from "react";
import * as Cesium from "cesium";

export function useFreeFlightCamera(viewer: Cesium.Viewer | null) {
  useEffect(() => {
    if (!viewer) return;

    const { scene, camera, clock } = viewer;
    const { screenSpaceCameraController } = scene;

    // LEFT_DRAG를 Look으로 리매핑 (기본 Orbit 대신 FPS Look)
    screenSpaceCameraController.lookEventTypes = [
      { eventType: Cesium.CameraEventType.LEFT_DRAG },
    ];
    screenSpaceCameraController.enableLook = true;

    // 관성 제거
    screenSpaceCameraController.inertiaSpin = 0;
    screenSpaceCameraController.inertiaTranslate = 0;
    screenSpaceCameraController.inertiaZoom = 0;
    screenSpaceCameraController.enableRotate = false;

    const keys = new Set<string>();
    const validKeys = new Set(["KeyW", "KeyA", "KeyS", "KeyD", "KeyE", "KeyQ"]);
    const velocity = new Cesium.Cartesian3(0, 0, 0);
    const dampingFactor = 0.85;

    const onKeyDown = (e: KeyboardEvent) => {
      if (validKeys.has(e.code)) keys.add(e.code);
    };
    const onKeyUp = (e: KeyboardEvent) => keys.delete(e.code);

    window.addEventListener("keydown", onKeyDown);
    window.addEventListener("keyup", onKeyUp);

    const tickListener = clock.onTick.addEventListener(() => {
      const position = camera.positionCartographic;
      // 지형 고도 조회 (fallback: 지형 데이터 미로드 시 position.height 사용)
      const terrainHeight = scene.globe.getHeight(position) ?? position.height;
      const relativeHeight = position.height - terrainHeight;
      const speed = Math.max(5.0, relativeHeight * 0.1);
      const dt =
        clock.clockStep === Cesium.ClockStep.TICK_DEPENDENT
          ? 1 / 60
          : clock.multiplier / 60;
      const distance = speed * dt;

      // camera.up을 지구 바깥 방향(법선)으로 유지
      const normal = Cesium.Ellipsoid.WGS84.geodeticSurfaceNormal(
        camera.position,
        new Cesium.Cartesian3(),
      );

      const direction = new Cesium.Cartesian3(0, 0, 0);
      let isMoving = false;

      if (keys.has("KeyW")) {
        Cesium.Cartesian3.add(direction, camera.direction, direction);
        isMoving = true;
      }
      if (keys.has("KeyS")) {
        Cesium.Cartesian3.subtract(direction, camera.direction, direction);
        isMoving = true;
      }
      if (keys.has("KeyA")) {
        const right = Cesium.Cartesian3.cross(
          camera.direction,
          camera.up,
          new Cesium.Cartesian3(),
        );
        Cesium.Cartesian3.subtract(direction, right, direction);
        isMoving = true;
      }
      if (keys.has("KeyD")) {
        const right = Cesium.Cartesian3.cross(
          camera.direction,
          camera.up,
          new Cesium.Cartesian3(),
        );
        Cesium.Cartesian3.add(direction, right, direction);
        isMoving = true;
      }

      if (keys.has("KeyE")) {
        Cesium.Cartesian3.add(direction, normal, direction);
        isMoving = true;
      }
      if (keys.has("KeyQ")) {
        Cesium.Cartesian3.subtract(direction, normal, direction);
        isMoving = true;
      }

      if (isMoving) {
        Cesium.Cartesian3.normalize(direction, direction);
        Cesium.Cartesian3.multiplyByScalar(direction, distance, velocity);
      } else {
        Cesium.Cartesian3.multiplyByScalar(velocity, dampingFactor, velocity);
      }

      // velocity 적용 - 새 객체를 생성하여 setter를 통해 할당
      camera.position = Cesium.Cartesian3.add(
        camera.position,
        velocity,
        new Cesium.Cartesian3(),
      );

      // 이동 후 up 벡터를 지구 법선 방향으로 재정렬 (롤 방지)
      const right = Cesium.Cartesian3.cross(
        camera.direction,
        normal,
        new Cesium.Cartesian3(),
      );
      if (Cesium.Cartesian3.magnitudeSquared(right) > 0) {
        Cesium.Cartesian3.normalize(right, right);
        const up = Cesium.Cartesian3.cross(
          right,
          camera.direction,
          new Cesium.Cartesian3(),
        );
        Cesium.Cartesian3.normalize(up, up);
        Cesium.Cartesian3.clone(up, camera.up);
      }
    });

    return () => {
      window.removeEventListener("keydown", onKeyDown);
      window.removeEventListener("keyup", onKeyUp);
      tickListener();
    };
  }, [viewer]);
}
