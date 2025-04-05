type TelemetryPoint = {
    t: number; // time
    x: number;
    y: number;
    z: number;
};

type Segment = {
    id: string;
    start: number;
    end: number;
    source: "auto" | "user";
};

type Types = {
    mp4: FileSystemFileHandle | null;
    lrv: FileSystemFileHandle | null;
    thm: FileSystemFileHandle | null;
    thumbnailUrl: string;
    status?: string;
    gyroData?: TelemetryPoint[];
    accelData?: TelemetryPoint[];
    segments?: Segment[];
    lastModified: number;
}
export type {Types, TelemetryPoint, Segment};