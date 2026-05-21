import { useEffect, useRef, useState, useCallback } from "react";
import { FireEvent, FirePosition } from "../types/fire";

interface UseFireSimulationProps {
  firePositionPool: FirePosition[];
  isPoolReady: boolean;
}

export function useFireSimulation({
  firePositionPool,
  isPoolReady,
}: UseFireSimulationProps) {
  const [fires, setFires] = useState<FireEvent[]>([]);
  const spawnTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const growthIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const scheduleNextSpawn = useCallback(() => {
    const delay = Math.random() * 4000 + 4000;
    spawnTimerRef.current = setTimeout(() => {
      const position =
        firePositionPool[Math.floor(Math.random() * firePositionPool.length)];
      const newFire: FireEvent = {
        id: Date.now().toString(),
        name: `fire-${Math.floor(Math.random() * 1000)}`,
        longitude: position.longitude,
        latitude: position.latitude,
        height: position.height,
        fireSize: 1,
        smokeHeight: 5,
        createdAt: Date.now(),
      };
      setFires((prev) => [...prev, newFire]);
      scheduleNextSpawn();
    }, delay);
  }, [firePositionPool]);

  useEffect(
    function startFireSimulation() {
      if (!isPoolReady || firePositionPool.length === 0) return;

      scheduleNextSpawn();

      growthIntervalRef.current = setInterval(function growFires() {
        setFires((prev) =>
          prev.map((fire) => ({
            ...fire,
            fireSize: Math.min(fire.fireSize + 1, 5),
            smokeHeight: Math.min(fire.smokeHeight + 5, 60),
          })),
        );
      }, 1000);

      return () => {
        if (spawnTimerRef.current !== null) clearTimeout(spawnTimerRef.current);
        if (growthIntervalRef.current !== null)
          clearInterval(growthIntervalRef.current);
      };
    },
    [isPoolReady, firePositionPool, scheduleNextSpawn],
  );

  const extinguish = useCallback((id: string) => {
    setFires((prev) => prev.filter((fire) => fire.id !== id));
  }, []);

  return { fires, extinguish };
}
