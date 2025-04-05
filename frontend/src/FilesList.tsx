import React from "react";

import {Types} from "./types.d.ts";

function formatFileSize(bytes: number): string {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
    if (bytes < 1024 * 1024 * 1024 * 1024) return `${(bytes / 1024 / 1024 / 1024).toFixed(2)} GB`;
    return `${(bytes / 1024 / 1024 / 1024 / 1024).toFixed(2)} TB`;
}


function formatDate(timestamp: number): string {
    return new Date(timestamp).toLocaleString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
    });
}

function FilesList({ files }: { files: Record<string, Types> }) {
    let totalSizeMp4 = 0;
    let totalSizeLrv = 0;
    let totalSizeThm = 0;
    files.map(([baseName, fileGroup]) => {
        if (fileGroup.mp4) totalSizeMp4 += fileGroup.mp4.size;
        if (fileGroup.lrv) totalSizeLrv += fileGroup.lrv.size;
        if (fileGroup.thm) totalSizeThm += fileGroup.thm.size;
    })

    return                 <table className="mt-4 table-auto border-collapse border border-gray-400 w-full">
        <thead>
        <tr className="bg-gray-100">
            <th className="border px-2 py-1">Base Name</th>
            <th className="border px-2 py-1">Created At</th>
            <th className="border px-2 py-1">MP4 ({formatFileSize(totalSizeMp4)})</th>
            <th className="border px-2 py-1">LRV ({formatFileSize(totalSizeLrv)})</th>
            <th className="border px-2 py-1">THM ({formatFileSize(totalSizeThm)})</th>
            <th className="border px-2 py-1">Status</th>
        </tr>
        </thead>
        <tbody>
        {files.map(([baseName, files]) => (
            <tr key={baseName}>
                <td className="border px-2 py-1">{baseName}</td>
                <td className="border px-2 py-1">{formatDate(files.lastModified)}</td>
                <td className="border px-2 py-1">
                    {files.mp4 ? `${files.mp4.name} (${formatFileSize(files.mp4.size)})` : "—"}
                </td>
                <td className="border px-2 py-1">
                    {files.lrv ? `${files.lrv.name} (${formatFileSize(files.lrv.size)})` : "—"}
                </td>
                <td className="border px-2 py-1">
                    {files.thm ? `${files.thm.name} (${formatFileSize(files.thm.size)})` : "—"}
                </td>
                <td className="border px-2 py-1">
                    {files.status ? files.status : "—"}
                </td>
            </tr>
        ))}
        </tbody>
    </table>
}

export type {Types};
export default FilesList;