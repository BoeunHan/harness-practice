import { useEffect, useRef, useState } from "react";
import * as Cesium from "cesium";

const SENSITIVITY = 0.001;

const CENTER_LONGITUDE = 127.026177;
const CENTER_LATITUDE = 37.501197;
const MAX_RADIUS = 600;
const MIN_HEIGHT = 5;
const MAX_HEIGHT = 300;
const MIN_GROUND_CLEARANCE = 5;

const validKeys = new Set([
  "KeyW",
  "KeyA",
  "KeyS",
  "KeyD",
  "KeyE",
  "KeyQ",
  "ShiftLeft",
]);

export function useFreeFlightCamera(viewer: Cesium.Viewer | null): {
  isLocked: boolean;
} {
  const [isLocked, setIsLocked] = useState(false);
  const isLockedRef = useRef(false);

  useEffect(() => {
    if (!viewer) return;

    const { scene, camera, clock } = viewer;
    const { screenSpaceCameraController } = scene;

    scene.globe.depthTestAgainstTerrain = true;

    const centerCartesian = Cesium.Cartesian3.fromDegrees(
      CENTER_LONGITUDE,
      CENTER_LATITUDE,
    );

    // 관성 제거 및 초기 설정
    screenSpaceCameraController.inertiaSpin = 0;
    screenSpaceCameraController.inertiaTranslate = 0;
    screenSpaceCameraController.inertiaZoom = 0;
    screenSpaceCameraController.enableRotate = false;
    screenSpaceCameraController.enableLook = false;

    const onClick = () => {
      viewer.canvas.requestPointerLock();
    };

    const onPointerLockChange = () => {
      const locked = document.pointerLockElement === viewer.canvas;
      isLockedRef.current = locked;
      setIsLocked(locked);
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isLockedRef.current) return;
      camera.lookRight(e.movementX * SENSITIVITY);
      camera.lookUp(-e.movementY * SENSITIVITY);
    };

    document.addEventListener("click", onClick);
    document.addEventListener("pointerlockchange", onPointerLockChange);
    document.addEventListener("mousemove", onMouseMove);

    const keys = new Set<string>();
    const velocity = new Cesium.Cartesian3(0, 0, 0);
    const dampingFactor = 0.85;

    const onKeyDown = (e: KeyboardEvent) => {
      if (validKeys.has(e.code)) keys.add(e.code);
    };
    const onKeyUp = (e: KeyboardEvent) => keys.delete(e.code);

    window.addEventListener("keydown", onKeyDown);
    window.addEventListener("keyup", onKeyUp);

    // 모든 카메라 위치 보정(제한)을 이 틱 레이어 내부에서 순차 처리
    const tickListener = clock.onTick.addEventListener(() => {
      if (!isLockedRef.current) return; // 락이 안 걸려있을 때는 비행 계산 안 함

      const position = camera.positionCartographic;
      // 지형 고도 조회 (fallback: 지형 데이터 미로드 시 position.height 사용)
      const terrainHeight = scene.globe.getHeight(position) ?? position.height;
      const relativeHeight = position.height - terrainHeight;
      let speed = Math.max(30.0, relativeHeight * 0.2);

      if (keys.has("ShiftLeft")) {
        speed *= 4.0;
      }

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
          normal,
          new Cesium.Cartesian3(),
        );
        Cesium.Cartesian3.subtract(direction, right, direction);
        isMoving = true;
      }
      if (keys.has("KeyD")) {
        const right = Cesium.Cartesian3.cross(
          camera.direction,
          normal,
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

      // 1. 새로운 속도 및 다음 좌표 계산
      if (isMoving && Cesium.Cartesian3.magnitudeSquared(direction) > 0) {
        Cesium.Cartesian3.normalize(direction, direction);
        Cesium.Cartesian3.multiplyByScalar(direction, distance, velocity);
      } else {
        Cesium.Cartesian3.multiplyByScalar(velocity, dampingFactor, velocity);
      }

      // 임시로 이동할 다음 좌표 계산
      let nextPosition = Cesium.Cartesian3.add(
        camera.position,
        velocity,
        new Cesium.Cartesian3(),
      );

      // 2. 이동 반영 전 경계선(600m) 체크 및 팅겨내기
      const dist = Cesium.Cartesian3.distance(nextPosition, centerCartesian);
      if (dist > MAX_RADIUS) {
        const dir = Cesium.Cartesian3.subtract(
          nextPosition,
          centerCartesian,
          new Cesium.Cartesian3(),
        );
        Cesium.Cartesian3.normalize(dir, dir);
        // 중심점 기준 600m 거리에 딱 달라붙게 강제 고정
        nextPosition = Cesium.Cartesian3.add(
          centerCartesian,
          Cesium.Cartesian3.multiplyByScalar(
            dir,
            MAX_RADIUS,
            new Cesium.Cartesian3(),
          ),
          new Cesium.Cartesian3(),
        );
        // 벽에 부딪혔으므로 속도 벡터 초기화
        Cesium.Cartesian3.clone(Cesium.Cartesian3.ZERO, velocity);
      }

      // 최종 계산된 좌표를 카메라에 대입
      camera.position = nextPosition;

      // 3. 고도 제한 및 지상고 보정 (최종 대입 후 갱신)
      const finalCarto = camera.positionCartographic;
      if (finalCarto.height > MAX_HEIGHT) {
        camera.position = Cesium.Cartesian3.fromRadians(
          finalCarto.longitude,
          finalCarto.latitude,
          MAX_HEIGHT,
        );
      } else if (finalCarto.height < MIN_HEIGHT) {
        camera.position = Cesium.Cartesian3.fromRadians(
          finalCarto.longitude,
          finalCarto.latitude,
          MIN_HEIGHT,
        );
      }

      const groundHeight = scene.sampleHeight(camera.positionCartographic);
      if (groundHeight !== undefined) {
        const minAllowed = groundHeight + MIN_GROUND_CLEARANCE;
        if (camera.positionCartographic.height < minAllowed) {
          camera.position = Cesium.Cartesian3.fromRadians(
            camera.positionCartographic.longitude,
            camera.positionCartographic.latitude,
            minAllowed,
          );
        }
      }

      // 4. 카메라 기울어짐(Roll) 방지 재정렬
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
      document.removeEventListener("click", onClick);
      document.removeEventListener("pointerlockchange", onPointerLockChange);
      document.removeEventListener("mousemove", onMouseMove);
      tickListener();
    };
  }, [viewer]);

  return { isLocked };
}
