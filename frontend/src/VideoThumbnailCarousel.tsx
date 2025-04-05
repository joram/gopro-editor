import React, {useEffect} from "react";
import {Types} from "./FilesList.tsx";
import "./VideoList.css";
import {Draggable} from "react-drag-reorder";
import Thumbnail from "./VideoThumbnailPrompt.tsx";
import InputFolderAccess from "./InputFolder.tsx";
import importGoProFolder from "./import.ts";

export default function VideoThumbnailCarousel() {
    let [files, setFiles] = React.useState<Types[]>([]);

    function newFileCallback(newFile: Types) {
        const newFiles = [...files];
        newFiles.push(newFile);
        setFiles(newFiles);
    }

    const thumbnails = [];
    for (let i = 0; i < files.length; i++) {
        const fileGroup = files[i];
        thumbnails.push(<Thumbnail
            fileSet={fileGroup}
            key={fileGroup.thumbnailUrl}
            status={fileGroup.status ? fileGroup.status : "unknown"}
        />)
    }

    return <>
        <button onClick={async () => {
            
                await importGoProFolder(dirHandle, newFileCallback)
            })
        }}>Import</button>
        <div className="thumbnail-carousel">
            <Draggable>
                {thumbnails}
            </Draggable>
        </div>
    </>
}
