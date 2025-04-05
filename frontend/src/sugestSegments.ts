import {TelemetryPoint, Segment, Types} from "./types.d.ts";
import {Buffer} from "buffer";
import gpmfExtract from "gpmf-extract";
import telemetry from "gopro-telemetry";


async function suggestSegments(fileset: Types, updateFileSet: any, maxSegments = 5): Segment[] {
    const threshold = 5;
    const interestPoints: number[] = [];

    if (!fileset.accelData || !fileset.gyroData){
        const {gyroData, accelData} = await extractData(fileset, updateFileSet);
        fileset.gyroData = gyroData;
        fileset.accelData = accelData;
    }

    const data = fileset.accelData;
    for (let i = 1; i < data.length; i++) {
        const delta =
            Math.abs(data[i].x - data[i - 1].x) +
            Math.abs(data[i].y - data[i - 1].y) +
            Math.abs(data[i].z - data[i - 1].z);

        if (delta > threshold) {
            interestPoints.push(data[i].t);
        }
    }

    if (interestPoints.length === 0) return [];

    // Group points into bursts based on proximity (e.g. ≤ 2s apart)
    const groups: number[][] = [];
    let currentGroup: number[] = [interestPoints[0]];

    for (let i = 1; i < interestPoints.length; i++) {
        const prev = interestPoints[i - 1];
        const curr = interestPoints[i];
        if (curr - prev <= 2) {
            currentGroup.push(curr);
        } else {
            groups.push(currentGroup);
            currentGroup = [curr];
        }
    }
    groups.push(currentGroup); // last group

    // Score groups by density
    const scored = groups.map((g) => ({
        points: g,
        score: g.length,
        start: Math.max(0, g[0] - 1),
        end: g[g.length - 1] + 1,
    }));

    // Sort by score (density)
    scored.sort((a, b) => b.score - a.score);

    const segments: Segment[] = [];

    const overlap = (a: { start: number; end: number }, b: { start: number; end: number }) =>
        a.end >= b.start && b.end >= a.start;

    for (const group of scored) {
        if (segments.length >= maxSegments) break;
        if (segments.some((s) => overlap(s, group))) continue;

        segments.push({
            id: crypto.randomUUID(),
            start: group.start,
            end: group.end,
            source: "auto",
        });
    }

    return segments.sort((a, b) => a.start - b.start);
}

export default suggestSegments;