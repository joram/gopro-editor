import {DefaultApi} from "./api-client/api";
import * as axios from "axios";

class ApiClient {
    _apiClient: DefaultApi | null = null;

    constructor() {
        let baseURL = "http://localhost:8000";
        // @ts-ignore
        if (process.env.NODE_ENV === "production") {
            baseURL = window.location.origin;
        }
        const axiosClient = axios.default.create({
            baseURL: baseURL,
            headers: {
                "Content-Type": "application/json",
            },
        });
        this._apiClient = new DefaultApi(undefined, baseURL, axiosClient);
    }

    getProjects() {
        if (!this._apiClient) {
            throw new Error("API client not initialized");
        }
        return this._apiClient.getProjectsApiProjectsGet()
    }

    getProject(projectSlug: string) {
        if (!this._apiClient) {
            throw new Error("API client not initialized");
        }
        return this._apiClient.getProjectApiProjectProjectSlugGet(projectSlug);
    }

    getVideos(projectSlug: string) {
        if (!this._apiClient) {
            throw new Error("API client not initialized");
        }
        return this._apiClient.getVideosApiProjectProjectSlugVideosGet(projectSlug);
    }

    getVideo(projectSlug: string, videoSlug: string) {
        if (!this._apiClient) {
            throw new Error("API client not initialized");
        }
        return this._apiClient.getVideoApiProjectProjectSlugVideoVideoSlugGet(projectSlug, videoSlug);
    }

    getSegments(projectSlug: string, videoSlug: string) {
        if (!this._apiClient) {
            throw new Error("API client not initialized");
        }
        return this._apiClient.getVideoApiProjectProjectSlugVideoVideoSlugGet(projectSlug, videoSlug);
    }

    buildFinalCut(projectSlug: string) {
        if (!this._apiClient) {
            throw new Error("API client not initialized");
        }
        return this._apiClient.buildFinalCutApiProjectProjectSlugFinalGet(projectSlug)
    }

    setSegments(projectSlug: string, videoSlug: string, segments: Array<any>) {
        if (!this._apiClient) {
            throw new Error("API client not initialized");
        }
        return this._apiClient.setVideoSegmentsApiProjectProjectSlugVideoVideoSlugSegmentsPost(projectSlug, videoSlug, segments);
    }
}

const apiClient = new ApiClient();

export default apiClient;