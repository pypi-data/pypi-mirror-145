import json
import math
import uuid
import datetime
from typing import List

import pytz

from ....enums.job_status import JobStatus
from ....enums.sensor_type import SensorType


class ReadingValueDto:
    sensorId: str
    type: str
    value: str
    measurementTime: str


class ReadingDto:
    printerId: str
    requestId: str
    readings: List[ReadingValueDto]
    measurementTime: str

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class MessageFactory:

    def create_sensor_registration_message(self, sensor_name: str, printer_id: str, sensor_type: SensorType):
        r_id = self._generate_uuid()
        reading = {
            'requestId': r_id,
            'printerId': printer_id,
            'sensorName': sensor_name,
            'sensorType': sensor_type,
            'measurementTime': self._get_date()
        }
        return reading, r_id

    def create_reading_message(self, sensor_id: str, sensor_type: SensorType, value: float, measured_at: datetime.datetime) -> ReadingValueDto:
        reading = ReadingValueDto()
        reading.sensorId = sensor_id
        reading.type = sensor_type.name
        reading.value = value
        reading.measurementTime = self._get_date(measured_at)
        return reading

    def create_reading_batch(self, readings: List[ReadingValueDto]) -> ReadingDto:
        reading = ReadingDto()
        reading.readings = readings
        reading.measurementTime = self._get_date()
        reading.requestId = self._generate_uuid()
        return reading

    def create_job_update_message(self, job_id: str, printer_id: str, status: JobStatus):
        job_update = {
            'jobId': job_id,
            'requestId': self._generate_uuid(),
            'printerId': printer_id,
            'status': status,
            'measurementTime': self._get_date()
        }
        return job_update

    def create_heartbeat_message(self, printer_id: str):
        heartbeat = {
            'printerId': printer_id,
            'requestId': self._generate_uuid(),
            'printerStatus': "CONNECTED",
            'measurementTime': self._get_date()
        }
        return heartbeat

    def _get_date(self, measured_at: datetime.datetime = None) -> str:
        if measured_at is None:
            measured_at = datetime.datetime.utcnow()
        value = pytz.utc.localize(measured_at)
        ms = round(math.floor(value.microsecond/10000)*10000)
        return value.replace(microsecond=ms).isoformat(timespec='milliseconds')

    def _generate_uuid(self) -> str:
        return str(uuid.uuid4())
