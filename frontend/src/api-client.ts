import {DefaultApi, Segment} from "./api-client/api";
import * as axios from "axios";

class ApiClient {
    _apiClient: DefaultApi | null = null;

    constructor() {
        const axiosClient = axios.default.create({
            baseURL: "http://localhost:8000",
            headers: {
                "Content-Type": "application/json",
            },
        });
        this._apiClient = new DefaultApi(undefined, "http://localhost:8000", axiosClient);
    }

    getProjects() {
        if (!this._apiClient) {
            throw new Error("API client not initialized");
        }
        return this._apiClient.getProjectsProjectsGet()
    }

    getProject(projectSlug: string) {
        if (!this._apiClient) {
            throw new Error("API client not initialized");
        }
        return this._apiClient.getProjectProjectProjectSlugGet(projectSlug);
    }

    getVideos(projectSlug: string) {
        if (!this._apiClient) {
            throw new Error("API client not initialized");
        }
        return this._apiClient.getVideosProjectProjectSlugVideosGet(projectSlug);
    }

    getVideo(projectSlug: string, videoSlug: string) {
        if (!this._apiClient) {
            throw new Error("API client not initialized");
        }
        return this._apiClient.getVideoProjectProjectSlugVideoVideoSlugGet(projectSlug, videoSlug);
    }

    getSegments(projectSlug: string, videoSlug: string) {
        if (!this._apiClient) {
            throw new Error("API client not initialized");
        }
        return this._apiClient.getVideoProjectProjectSlugVideoVideoSlugGet(projectSlug, videoSlug);
    }

    setSegments(projectSlug: string, videoSlug: string, segments: Array<Segment>) {
        if (!this._apiClient) {
            throw new Error("API client not initialized");
        }
        return this._apiClient.setVideoSegmentsProjectProjectSlugVideoVideoSlugSegmentsPost(projectSlug, videoSlug, segments);
    }
}

const apiClient = new ApiClient();

export default apiClient;