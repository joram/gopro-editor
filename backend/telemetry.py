import os
import numpy as np

from py_gpmf_parser import GoProTelemetryExtractor
from pydantic import BaseModel


class Telemetry(BaseModel):
    gyro: list
    accel: list
    raw_accel_data: list
    raw_gyro_data: list
    accel_timestamps: list


def get_telemetry(filepath) -> Telemetry:
    extractor = GoProTelemetryExtractor(filepath)
    extractor.open_source()
    [raw_accel_data, accel_timestamps] = extractor.extract_data('ACCL')
    [raw_gyro_data, gyro_timestamps] = extractor.extract_data('GYRO')
    extractor.close_source()

    # Convert raw data to a list of dictionaries
    def convert_to_dict(data, timestamp):
        return {
            "timestamp": timestamp,
            "x": data[0],
            "y": data[1],
            "z": data[2],
        }

    accel = []
    i = 0
    for data in raw_accel_data:
        accel.append(convert_to_dict(data, accel_timestamps[i]))
        i += 1

    gyro = []
    i = 0
    for data in raw_gyro_data:
        gyro.append(convert_to_dict(data, gyro_timestamps[i]))
        i += 1

    return Telemetry(accel=accel, gyro=gyro, raw_accel_data=raw_accel_data, raw_gyro_data=raw_gyro_data, accel_timestamps=accel_timestamps)


