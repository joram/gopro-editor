import { Types, TelemetryPoint } from "./types.d.ts";
import { Buffer } from "buffer";
import gpmfExtract from "gpmf-extract";
import telemetry from "gopro-telemetry";

async function getThumbnailUrl(file: File): Promise<string> {
    const reader = file.stream().getReader();
    const chunks: Uint8Array[] = [];

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        if (value) chunks.push(value);
    }

    const blob = new Blob(chunks, { type: "image/jpeg" });
    const url = URL.createObjectURL(blob);
    return url;
}

async function extractData(file: File) {

    const formatPoints = (samples: any): TelemetryPoint[] => {
        return samples.map((s: any) => ({
            t: s.cts / 1000,
            x: s.value[0],
            y: s.value[1],
            z: s.value[2],
        }));
    };

    const arrayBuffer = await file.arrayBuffer();

    const nodeBuffer = Buffer.from(arrayBuffer);
    const cancellationToken = { cancelled: false };

    try {
        const extracted = await gpmfExtract(nodeBuffer, {
            browserMode: true,
            cancellationToken,
        });

        const result = await telemetry(extracted, { stream: ["GYRO", "ACCL"] });

        let gyroData: TelemetryPoint[] = [];
        if (result && result[1].streams.GYRO) {
            gyroData = formatPoints(result[1].streams.GYRO.samples);
        }

        let accelData: TelemetryPoint[] = [];
        if (result && result[1].streams.ACCL) {
            accelData = formatPoints(result[1].streams.ACCL.samples);
        }

        return { gyroData, accelData };
    } catch (error) {
        return { gyroData: [], accelData: [] };
    }
}

async function importGoProFile(filename: string, mp4File: File, dirHandle: FileSystemDirectoryHandle): Promise<Types> {

    const thmFileName = filename.replace(/\.MP4$/, ".THM");
    const lvrFileName = filename.replace(/\.MP4$/, ".LRV").replace("GX", "GL");
    const gyroFileName = filename.replace(/\.MP4$/, ".gyro.json");
    const accelFileName = filename.replace(/\.MP4$/, ".accel.json");
    const segmentsFileName = filename.replace(/\.MP4$/, ".segments.json");

    const thmFileHandle = await dirHandle.getFileHandle(thmFileName, { create: false });
    const gyroFileHandle = await dirHandle.getFileHandle(gyroFileName, { create: true });
    const accelFileHandle = await dirHandle.getFileHandle(accelFileName, { create: true });
    const segmentsFileHandle = await dirHandle.getFileHandle(segmentsFileName, { create: true });

    const fileSet: Types = {
        lastModified: mp4File.lastModified,
        mp4: mp4File,
        thm: thmFileHandle,
        status: "Not processed",
        segments: [],
        thumbnailUrl: ""
    };

    const gyroFile = await gyroFileHandle.getFile();

    if (gyroFile.size === 0) {
        const { gyroData, accelData } = await extractData(mp4File);

        const gyroWriter = await gyroFileHandle.createWritable();
        await gyroWriter.write(JSON.stringify(gyroData));
        await gyroWriter.close();

        const accelWriter = await accelFileHandle.createWritable();
        await accelWriter.write(JSON.stringify(accelData));
        await accelWriter.close();

        fileSet.gyroData = gyroData;
        fileSet.accelData = accelData;
    } else {
        const gyroData = await gyroFileHandle.getFile();
        const accelData = await accelFileHandle.getFile();
        fileSet.gyroData = JSON.parse(await gyroData.text());
        fileSet.accelData = JSON.parse(await accelData.text());
    }

    fileSet.thumbnailUrl = await getThumbnailUrl(await thmFileHandle.getFile());
    return fileSet;
}


async function importGoProFolder(dirHandle, newFileCallback) {

    async function walkDirectory(handle: FileSystemDirectoryHandle, path = ""): Promise<{ filename: string, file: File, fullPath: string }[]> {
        const files: { filename: string, file: File, fullPath: string }[] = [];

        for await (const [name, entry] of handle.entries()) {
            const currentPath = `${path}${name}`;
            if (entry.kind === "file" && name.toLowerCase().endsWith(".mp4")) {
                const file = await entry.getFile();
                files.push({filename: name, file, fullPath: currentPath });
            }
        }
        return files;
    }

    const allFiles = await walkDirectory(dirHandle);
    allFiles.forEach(({filename, file}) => {
        importGoProFile(filename, file, dirHandle).then((fileSet) => {
            newFileCallback(fileSet);
        })
    })
}

export default importGoProFolder;
