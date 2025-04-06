# Video


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_dir_name** | **string** |  | [default to undefined]
**length** | **number** |  | [default to undefined]
**size_bytes** | **number** |  | [default to undefined]
**slug** | **string** |  | [default to undefined]
**mp4_filename** | **string** |  | [default to undefined]
**lrv_filename** | **string** |  | [default to undefined]
**thumbnail_filename** | **string** |  | [default to undefined]
**accel_filename** | **string** |  | [default to undefined]
**gyro_filename** | **string** |  | [default to undefined]
**segments_filename** | **string** |  | [default to undefined]
**suggested_segments** | [**Array&lt;Segment&gt;**](Segment.md) |  | [optional] [default to undefined]
**interest_levels** | [**Array&lt;InterestLevel&gt;**](InterestLevel.md) |  | [optional] [default to undefined]
**accel** | **Array&lt;{ [key: string]: any; }&gt;** |  | [optional] [default to undefined]
**gyro** | **Array&lt;{ [key: string]: any; }&gt;** |  | [optional] [default to undefined]
**segments** | [**Array&lt;Segment&gt;**](Segment.md) |  | [optional] [default to undefined]

## Example

```typescript
import { Video } from './api';

const instance: Video = {
    project_dir_name,
    length,
    size_bytes,
    slug,
    mp4_filename,
    lrv_filename,
    thumbnail_filename,
    accel_filename,
    gyro_filename,
    segments_filename,
    suggested_segments,
    interest_levels,
    accel,
    gyro,
    segments,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
