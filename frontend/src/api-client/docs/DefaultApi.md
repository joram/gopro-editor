# DefaultApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**getProjectProjectProjectSlugGet**](#getprojectprojectprojectslugget) | **GET** /project/{project_slug} | Get Project|
|[**getProjectsProjectsGet**](#getprojectsprojectsget) | **GET** /projects | Get Projects|
|[**getVideoProjectProjectSlugVideoVideoSlugGet**](#getvideoprojectprojectslugvideovideoslugget) | **GET** /project/{project_slug}/video/{video_slug} | Get Video|
|[**getVideoSegmentsProjectProjectSlugVideoVideoSlugSegmentsGet**](#getvideosegmentsprojectprojectslugvideovideoslugsegmentsget) | **GET** /project/{project_slug}/video/{video_slug}/segments | Get Video Segments|
|[**getVideosProjectProjectSlugVideosGet**](#getvideosprojectprojectslugvideosget) | **GET** /project/{project_slug}/videos | Get Videos|
|[**setVideoSegmentsProjectProjectSlugVideoVideoSlugSegmentsPost**](#setvideosegmentsprojectprojectslugvideovideoslugsegmentspost) | **POST** /project/{project_slug}/video/{video_slug}/segments | Set Video Segments|

# **getProjectProjectProjectSlugGet**
> Project getProjectProjectProjectSlugGet()


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

let projectSlug: string; // (default to undefined)

const { status, data } = await apiInstance.getProjectProjectProjectSlugGet(
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

# **getProjectsProjectsGet**
> Array<Project> getProjectsProjectsGet()


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

const { status, data } = await apiInstance.getProjectsProjectsGet();
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

# **getVideoProjectProjectSlugVideoVideoSlugGet**
> Video getVideoProjectProjectSlugVideoVideoSlugGet()


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

const { status, data } = await apiInstance.getVideoProjectProjectSlugVideoVideoSlugGet(
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

# **getVideoSegmentsProjectProjectSlugVideoVideoSlugSegmentsGet**
> Array<Segment> getVideoSegmentsProjectProjectSlugVideoVideoSlugSegmentsGet()


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

const { status, data } = await apiInstance.getVideoSegmentsProjectProjectSlugVideoVideoSlugSegmentsGet(
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

**Array<Segment>**

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

# **getVideosProjectProjectSlugVideosGet**
> Array<Video> getVideosProjectProjectSlugVideosGet()


### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

let projectSlug: string; // (default to undefined)

const { status, data } = await apiInstance.getVideosProjectProjectSlugVideosGet(
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

# **setVideoSegmentsProjectProjectSlugVideoVideoSlugSegmentsPost**
> Video setVideoSegmentsProjectProjectSlugVideoVideoSlugSegmentsPost(segment)


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

const { status, data } = await apiInstance.setVideoSegmentsProjectProjectSlugVideoVideoSlugSegmentsPost(
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

