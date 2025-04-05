import React from "react";
import InputFolderAccess from "./InputFolder.tsx";
import FilesList, {Types} from "./FilesList.tsx";
import VideoThumbnailCarousel from "./VideoThumbnailCarousel.tsx";
import suggestSegments from "./sugestSegments.ts";

function SuggestSnippets({files, setFiles}: { files: Types[], setFiles: any }) {
    function getFirstUnprocessedFile(files: Types[]) {
        for (let i = 0; i < files.length; i++) {
            if (files[i].status === "Not processed") {
                return [i, files[i]];
            }
        }
        return null;
    }


    async function calculateSuggestedSnippets() {
        let [firstUnprocessedFileIndex, firstUnprocessedFile] = getFirstUnprocessedFile(files);
        if (!firstUnprocessedFile) {
            return null;
        }

        function updateUnprocessedFile(updatedFile) {
            files[firstUnprocessedFileIndex] = updatedFile;
            setFiles(files);
        }

        while(getFirstUnprocessedFile(files) !== null) {
            [firstUnprocessedFileIndex, firstUnprocessedFile] = getFirstUnprocessedFile(files)
            const suggestedSegments = await suggestSegments(firstUnprocessedFile, updateUnprocessedFile)
            console.log("suggestedSegments for ", firstUnprocessedFile.mp4.name, ": ", suggestedSegments)
            firstUnprocessedFile.segments = suggestedSegments;
            firstUnprocessedFile.status = "Processed";
            updateUnprocessedFile(firstUnprocessedFile);
        }
    }

    if (getFirstUnprocessedFile(files) !== null) {
        return <>
            <button onClick={async () => calculateSuggestedSnippets()}>Suggest Snippets</button>
        </>
    }

}

function App() {
    return <VideoThumbnailCarousel />
}

export default App;
