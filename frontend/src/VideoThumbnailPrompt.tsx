import React from "react";
import {Types} from "./types.d.ts";

type ThumbnailProps = {
    status: string;
    fileSet: Types;
};

function Thumbnail({ fileSet, status }: ThumbnailProps) {
    return (
        <div
            className="thumbnail-container"
            style={{
                position: "relative",
                width: 160,
                borderRadius: 8,
                overflow: "hidden",
                boxShadow: "0 2px 8px rgba(0, 0, 0, 0.2)",
                marginRight: "1rem",
            }}
        >
            <img
                src={fileSet.thumbnailUrl}
                alt="thumbnail"
                style={{
                    width: "100%",
                    display: "block",
                }}
            />
            {fileSet.status && (
                <div
                    className="status-overlay"
                    style={{
                        position: "absolute",
                        bottom: 0,
                        width: "100%",
                        backgroundColor: "rgba(0, 0, 0, 0.6)",
                        color: "white",
                        textAlign: "center",
                        padding: "0.25rem 0.5rem",
                        fontSize: "0.9rem",
                    }}
                >
                    {status}
                </div>
            )}
        </div>
    );
}

export default Thumbnail;