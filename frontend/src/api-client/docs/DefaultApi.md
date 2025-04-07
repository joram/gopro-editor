# DefaultApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**buildFinalCutApiProjectProjectSlugFinalGet**](#buildfinalcutapiprojectprojectslugfinalget) | **GET** /api/project/{project_slug}/final | Build Final Cut|
|[**getProjectApiProjectProjectSlugCalculateGet**](#getprojectapiprojectprojectslugcalculateget) | **GET** /api/project/{project_slug}/calculate | Get Project|
|[**getProjectApiProjectProjectSlugGet**](#getprojectapiprojectprojectslugget) | **GET** /api/project/{project_slug} | Get Project|
|[**getProjectsApiProjectsGet**](#getprojectsapiprojectsget) | **GET** /api/projects | Get Projects|
|[**getVideoApiProjectProjectSlugVideoVideoSlugGet**](#getvideoapiprojectprojectslugvideovideoslugget) | **GET** /api/project/{project_slug}/video/{video_slug} | Get Video|
|[**getVideoPreviewApiProjectProjectSlugVideoVideoSlugPreviewGet**](#getvideopreviewapiprojectprojectslugvideovideoslugpreviewget) | **GET** /api/project/{project_slug}/video/{video_slug}/preview | Get Video Preview|
|[**getVideoSegmentsApiProjectProjectSlugVideoVideoSlugThumbnailGet**](#getvideosegmentsapiprojectprojectslugvideovideoslugthumbnailget) | **GET** /api/project/{project_slug}/video/{video_slug}/thumbnail | Get Video Segments|
|[**getVideosApiProjectProjectSlugVideosGet**](#getvideosapiprojectprojectslugvideosget) | **GET** /api/project/{project_slug}/videos | Get Videos|
|[**rootGet**](#rootget) | **GET** / | Root|
|[**serveReactAppFilepathGet**](#servereactappfilepathget) | **GET** /{filepath} | Serve React App|
|[**setVideoSegmentsApiProjectProjectSlugVideoVideoSlugSegmentsPost**](#setvideosegmentsapiprojectprojectslugvideovideoslugsegmentspost) | **POST** /api/project/{project_slug}/video/{video_slug}/segments | Set Video Segments|

# **buildFinalCutApiProjectProjectSlugFinalGet**
> any buildFinalCutApiProjectProjectSlugFinalGet()


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

let projectSlug: string; // (default to undefined)

const { status, data } = await apiInstance.buildFinalCutApiProjectProjectSlugFinalGet(
    projectSlug
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projectSlug** | [**string**] |  | defaults to undefined|


### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getProjectApiProjectProjectSlugCalculateGet**
> Project getProjectApiProjectProjectSlugCalculateGet()


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

let projectSlug: string; // (default to undefined)

const { status, data } = await apiInstance.getProjectApiProjectProjectSlugCalculateGet(
    projectSlug
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projectSlug** | [**string**] |  | defaults to undefined|


### Return type

**Project**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getProjectApiProjectProjectSlugGet**
> Project getProjectApiProjectProjectSlugGet()


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

let projectSlug: string; // (default to undefined)

const { status, data } = await apiInstance.getProjectApiProjectProjectSlugGet(
    projectSlug
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projectSlug** | [**string**] |  | defaults to undefined|


### Return type

**Project**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getProjectsApiProjectsGet**
> Array<Project> getProjectsApiProjectsGet()


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

const { status, data } = await apiInstance.getProjectsApiProjectsGet();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**Array<Project>**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getVideoApiProjectProjectSlugVideoVideoSlugGet**
> Video getVideoApiProjectProjectSlugVideoVideoSlugGet()


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

let projectSlug: string; // (default to undefined)
let videoSlug: string; // (default to undefined)

const { status, data } = await apiInstance.getVideoApiProjectProjectSlugVideoVideoSlugGet(
    projectSlug,
    videoSlug
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projectSlug** | [**string**] |  | defaults to undefined|
| **videoSlug** | [**string**] |  | defaults to undefined|


### Return type

**Video**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getVideoPreviewApiProjectProjectSlugVideoVideoSlugPreviewGet**
> any getVideoPreviewApiProjectProjectSlugVideoVideoSlugPreviewGet()


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

let projectSlug: string; // (default to undefined)
let videoSlug: string; // (default to undefined)

const { status, data } = await apiInstance.getVideoPreviewApiProjectProjectSlugVideoVideoSlugPreviewGet(
    projectSlug,
    videoSlug
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projectSlug** | [**string**] |  | defaults to undefined|
| **videoSlug** | [**string**] |  | defaults to undefined|


### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getVideoSegmentsApiProjectProjectSlugVideoVideoSlugThumbnailGet**
> any getVideoSegmentsApiProjectProjectSlugVideoVideoSlugThumbnailGet()


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

let projectSlug: string; // (default to undefined)
let videoSlug: string; // (default to undefined)

const { status, data } = await apiInstance.getVideoSegmentsApiProjectProjectSlugVideoVideoSlugThumbnailGet(
    projectSlug,
    videoSlug
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projectSlug** | [**string**] |  | defaults to undefined|
| **videoSlug** | [**string**] |  | defaults to undefined|


### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getVideosApiProjectProjectSlugVideosGet**
> Array<Video> getVideosApiProjectProjectSlugVideosGet()


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

let projectSlug: string; // (default to undefined)

const { status, data } = await apiInstance.getVideosApiProjectProjectSlugVideosGet(
    projectSlug
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projectSlug** | [**string**] |  | defaults to undefined|


### Return type

**Array<Video>**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **rootGet**
> any rootGet()


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

const { status, data } = await apiInstance.rootGet();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **serveReactAppFilepathGet**
> any serveReactAppFilepathGet()


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

let filepath: string; // (default to undefined)

const { status, data } = await apiInstance.serveReactAppFilepathGet(
    filepath
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **filepath** | [**string**] |  | defaults to undefined|


### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **setVideoSegmentsApiProjectProjectSlugVideoVideoSlugSegmentsPost**
> Video setVideoSegmentsApiProjectProjectSlugVideoVideoSlugSegmentsPost(segment)


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

let projectSlug: string; // (default to undefined)
let videoSlug: string; // (default to undefined)
let segment: Array<Segment>; //

const { status, data } = await apiInstance.setVideoSegmentsApiProjectProjectSlugVideoVideoSlugSegmentsPost(
    projectSlug,
    videoSlug,
    segment
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **segment** | **Array<Segment>**|  | |
| **projectSlug** | [**string**] |  | defaults to undefined|
| **videoSlug** | [**string**] |  | defaults to undefined|


### Return type

**Video**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

