import React from "react";
import "./InputFolder.css"
import importGoProFolder from "./import.ts";


function InputFolderAccess({ newFileCallback }: { newFileCallback:any}) {
    async function getFilesFromFolder() {

    }
    return (
        <button className="input-folder-access" onClick={getFilesFromFolder}>Select input folder</button>
    );
}

export default InputFolderAccess;
