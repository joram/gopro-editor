import os
from http.client import HTTPException
from typing import List

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import Response
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import FileResponse, RedirectResponse

from models import get_all_projects, get_project as get_p, Project, Video, Segment
from process_segments import process_videos

sentry_sdk.init(
    dsn="https://e88a3329c652d147a4947c6eb3af0539@o4509101771259904.ingest.us.sentry.io/4509101773029376",
    send_default_pii=True,
    traces_sample_rate=1.0,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from starlette.staticfiles import StaticFiles
from starlette.responses import Response

class CORPStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response: Response = await super().get_response(path, scope)
        response.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
        return response

# Then mount using the custom class
app.mount("/static/projects/", StaticFiles(directory="projects"), name="projects")
app.mount("/assets/", StaticFiles(directory="static/assets"), name="assets")


@app.get("/")
async def root():
    return RedirectResponse(url="/projects")


@app.get("/api/projects")
async def get_projects() -> list[Project]:
    return get_all_projects()


@app.get("/api/project/{project_slug}")
async def get_project(project_slug: str) -> Project:
    project = get_p(project_slug)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.get("/api/project/{project_slug}/calculate")
async def get_project(project_slug: str) -> Project:
    project = get_p(project_slug)
    for video in project.videos:
        video.calculate_suggested_segments()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.get("/api/project/{project_slug}/videos")
async def get_videos(project_slug: str) -> List[Video]:
    project = get_p(project_slug)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.videos


@app.get("/api/project/{project_slug}/video/{video_slug}")
async def get_video(project_slug: str, video_slug: str) -> Video:
    project = get_p(project_slug)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    for video in project.videos:
        if video.slug == video_slug:
            video.calculate_suggested_segments()
            return video
    raise HTTPException(status_code=404, detail="Video not found")


@app.get("/api/project/{project_slug}/final")
async def build_final_cut(
    project_slug: str
) -> None:
    project = get_p(project_slug)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    process_videos(project.videos)



@app.post("/api/project/{project_slug}/video/{video_slug}/segments")
async def set_video_segments(
    project_slug: str, video_slug: str, segments: List[Segment]
) -> Video:
    project = get_p(project_slug)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    for video in project.videos:
        if video.slug == video_slug:
            video.calculate_suggested_segments()
            video.segments = segments
            video.write_segments()
            return video
    raise HTTPException(status_code=404, detail="Video not found")


@app.get("/api/project/{project_slug}/video/{video_slug}/thumbnail")
async def get_video_segments(project_slug: str, video_slug: str) -> FileResponse:
    project = get_p(project_slug)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    for video in project.videos:
        if video.slug == video_slug:
            if video.thumbnail_filename is not None:
                return FileResponse(
                    os.path.join("./projects", project.name, video.thumbnail_filename),
                    media_type="image/jpeg",
                    filename=video.thumbnail_filename,
                    headers={
                        "Content-Disposition": f"inline; filename={video.thumbnail_filename}",
                        "Cross-Origin-Embedder-Policy": "require-corp",
                        "Cross-Origin-Resource-Policy": "*",
                    }
                )

    raise HTTPException(status_code=404, detail="Video not found")


@app.get("/api/project/{project_slug}/video/{video_slug}/preview")
async def get_video_preview(project_slug: str, video_slug: str) -> FileResponse:
    project = get_p(project_slug)
    for video in project.videos:
        if video.slug == video_slug:
            if video.lrv_filename is not None:
                return FileResponse(
                    os.path.join("./projects", project.name, video.lrv_filename),
                    media_type="video/mp4",
                    filename=video.lrv_filename,
                    headers={
                        "Content-Disposition": f"inline; filename={video.lrv_filename}",
                        "Cross-Origin-Embedder-Policy": "require-corp",
                        "Cross-Origin-Resource-Policy": "*",
                    }
                )


@app.get("/{filepath:path}")
async def serve_react_app(filepath: str, request: Request):
    index_path = os.path.join("static", "index.html")
    return FileResponse(index_path)

