import React from "react";

type FileSet = {
    mp4: File | null;
    lrv: File | null;
    thm: File | null;
    lastModified: number; // used for sorting
};

function InputFolderAccess({ setVideoFiles }: { setVideoFiles: (files: Record<string, FileSet>) => void }) {
    const getFilesFromFolder = async () => {
        try {
            const dirHandle = await window.showDirectoryPicker();
            const fileBunches: Record<string, FileSet> = {};

            for await (const [name, handle] of dirHandle.entries()) {
                if (handle.kind === "file") {
                    const file = await handle.getFile();
                    const parts = file.name.split(".");
                    if (parts.length < 2) continue;

                    const extension = parts.pop()?.toLowerCase();
                    let baseName = parts.join(".");
                    baseName = baseName.replace(/^(GL|GX)/i, "");

                    if (!fileBunches[baseName]) {
                        fileBunches[baseName] = { mp4: null, lrv: null, thm: null, lastModified: file.lastModified };
                    }

                    // Update timestamp if earlier than existing (use earliest file as representative)
                    if (file.lastModified < fileBunches[baseName].lastModified) {
                        fileBunches[baseName].lastModified = file.lastModified;
                    }

                    if (extension === "mp4") fileBunches[baseName].mp4 = file;
                    if (extension === "lrv") fileBunches[baseName].lrv = file;
                    if (extension === "thm") fileBunches[baseName].thm = file;
                }
            }

            setVideoFiles(fileBunches);
        } catch (err) {
            console.error("Folder access cancelled or failed:", err);
        }
    };

    return (
        <button onClick={getFilesFromFolder}>Select input folder</button>
    );
}

function formatFileSize(bytes: number): string {
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
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


function App() {
    const [videoFiles, setVideoFiles] = React.useState<Record<string, FileSet>>({});

    const sortedFiles = Object.entries(videoFiles)
        .sort(([, a], [, b]) => a.lastModified - b.lastModified);

    return (
        <div className="p-4">
            <InputFolderAccess setVideoFiles={setVideoFiles} />
            {sortedFiles.length > 0 && (
                <table className="mt-4 table-auto border-collapse border border-gray-400 w-full">
                    <thead>
                    <tr className="bg-gray-100">
                        <th className="border px-2 py-1">Base Name</th>
                        <th className="border px-2 py-1">Created At</th>
                        <th className="border px-2 py-1">MP4</th>
                        <th className="border px-2 py-1">LRV</th>
                        <th className="border px-2 py-1">THM</th>
                    </tr>
                    </thead>
                    <tbody>
                    {sortedFiles.map(([baseName, files]) => (
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
                        </tr>
                    ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default App;
