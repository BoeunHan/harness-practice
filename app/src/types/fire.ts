export interface FirePosition {
  longitude: number;
  latitude: number;
  height: number;
}

export interface FireEvent {
  id: string;
  name: string;
  longitude: number;
  latitude: number;
  height: number;
  fireSize: number;
  smokeHeight: number;
  createdAt: number;
}
