import React from "react";
import {Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";
import {Types} from "./FilesList.tsx";
import {TelemetryPoint} from "./types.d.ts";

export function TelemetryViewer({ fileSet }: { fileSet: Types }) {


    if (!fileSet) {
        return null
    }
    if (!fileSet.mp4) {
        return null
    }

    return (
        <div className="p-4">
            <h2 className="text-lg font-bold mb-2">Gyroscope</h2>
            <Chart data={fileSet.gyroData} />
            <h2 className="text-lg font-bold mt-6 mb-2">Accelerometer</h2>
            <Chart data={fileSet.accelData} />
        </div>
    );
}

function Chart({ data }: { data: TelemetryPoint[] }) {
    return (
        <ResponsiveContainer width="100%" height={200}>
            <LineChart data={data}>
                <XAxis dataKey="t" label={{ value: "Time (s)", position: "insideBottomRight", offset: -5 }} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="x" stroke="#8884d8" dot={false} />
                <Line type="monotone" dataKey="y" stroke="#82ca9d" dot={false} />
                <Line type="monotone" dataKey="z" stroke="#ffc658" dot={false} />
            </LineChart>
        </ResponsiveContainer>
    );
}

export default TelemetryViewer;