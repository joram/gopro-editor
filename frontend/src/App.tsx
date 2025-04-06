import React, {useEffect} from "react";
import apiClient from "./api-client.ts";
import {BrowserRouter, Route, Routes, useParams} from "react-router";
import {VideoWithInterestGraph} from "./TelemetryViewer.tsx";
import "./App.css"


function secondsToHMS(seconds: number) {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);

    if(h > 0) {
        return `${h}:${m}:${s}`;
    }
    return `${m}:${s}`;
}

function ProjectsList() {
    // @ts-ignore
    const [projects, setProjects]: [Project[], any] = React.useState(null);

    useEffect(() => {
        apiClient.getProjects().then(response => {
            console.log("Projects: ", response.data);
            setProjects(response.data);
        })

    }, []);

    if (!projects) {
        return <div>Loading...</div>;
    }

    const projectLinks = projects.map((project: any) => {
        return <a href={"/project/"+project.slug} key={project.slug}>{project.name}</a>
    })
    return <div>
        <h1>Projects</h1>
        {projectLinks}
    </div>
}

function ProjectPage() {
    const params = useParams();
    const projectSlug = params.projectSlug;

    let [project, setProject]: [any, any] = React.useState(null);

    useEffect(() => {
        if (!projectSlug) {
            return;
        }
        apiClient.getProject(projectSlug).then(response => {
            setProject(response.data);
        })

    }, []);


    if (!project) {
        return <div>Loading...</div>;
    }

    let totalSegments = 0;
    let totalSegmentsDuration = 0;
    let totalDuration = 0;
    project.videos.forEach((video: any) => {
        totalDuration += video.length;
        video.segments.forEach((segment: any) => {
            totalSegments++;
            totalSegmentsDuration += segment.end_time - segment.start_time;
        })
    })

    console.log(project)
    return <>
        <h1>Project: {project.name}</h1>
        <h2>Videos</h2>
        <table>
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Thumbnail</th>
                    <th>Num Segments ({totalSegments})</th>
                    <th>Segments Total Duration ({secondsToHMS(totalSegmentsDuration)})</th>
                    <th>Duration ({secondsToHMS(totalDuration)})</th>
                </tr>
            </thead>
            {project.videos.map((video: any) => {
                let videosSegmentsDurations = 0;
                video.segments.forEach((segment: any) => {
                    console.log(segment)
                    videosSegmentsDurations += segment.end_time - segment.start_time;
                })


                return <tr key={video.slug}>
                    <td><a href={"/project/"+projectSlug+"/video/"+video.slug}>{video.mp4_filename}</a></td>
                    <td><img src={"/project/"+projectSlug+"/video/"+video.slug+"/thumbnail"} alt="thumbnail" width="100"/></td>
                    <td>{video.segments.length}</td>
                    <td>{secondsToHMS(videosSegmentsDurations)}</td>
                    <td>{secondsToHMS(video.length)}</td>
                </tr>
            })}
        </table>
    </>
}

function VideoPage() {
    const params = useParams();
    const projectSlug = params.projectSlug;
    const videoSlug = params.videoSlug;
    let [video, setVideo]: [any, any] = React.useState(null);

    useEffect(() => {
        if (!projectSlug || !videoSlug) {
            return;
        }
        apiClient.getVideo(projectSlug, videoSlug).then(response => {
            setVideo(response.data);
        })

    }, []);
    if (!video) {
        return <div>Loading...</div>;
    }
    console.log(video)
    const url = `http://localhost:8000/project/${projectSlug}/video/${videoSlug}/preview`;
    return <div className="max-h-screen">
        <VideoWithInterestGraph videoUrl={url} interestData={video.interest_levels} suggestedSegments={video.suggested_segments}  projectSlug={projectSlug} videoSlug={videoSlug} />
        </div>
}

function App() {
    return <BrowserRouter>
        <Routes>
            <Route path="/" element={<ProjectsList />} />
            <Route path="/projects" element={<ProjectsList />} />
            <Route path="/project/:projectSlug" element={<ProjectPage />} />
            <Route path="/project/:projectSlug/video/:videoSlug" element={<VideoPage />} />
        </Routes>
    </BrowserRouter>

}

export default App;
