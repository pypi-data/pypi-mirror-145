from io import BytesIO

import requests

VALID_MEASUREMENTS = [
    'MEAN_ARTERIAL_PRESSURE',
    'DIASTOLIC',
    'SYSTOLIC',
    'PULSE',
    'BLOOD_OXYGEN',
    'WEIGHT',
    'HEIGHT',
    'TEMPERATURE',
    'RESPIRATORY_RATE'
]

IMAGE_FILE_EXTENSIONS = ['.jpg', '.jpeg', '.png']


def filter_measurements_with_picture(measurement):
    value = measurement.get('value', {})
    return (value.get('file') and
            isinstance(value.get('file'), str) and
            value.get('fileType', '') in IMAGE_FILE_EXTENSIONS and
            value.get('status', '') == 'AVAILABLE')


def get_measurements_pictures(measurements_list):
    detected_measurements = set()
    images = []
    for measurement in filter(filter_measurements_with_picture, measurements_list):
        value = measurement.get('value')
        friendly_body_part_name = '{} {}'.format(
            value.get('bodySide'),
            value.get('bodyPart')
        )
        if friendly_body_part_name not in detected_measurements:
            try:
                media_response = requests.get(value.get('file'))
                if media_response.ok:
                    images.append({
                        'title': friendly_body_part_name,
                        'media': BytesIO(media_response.content)
                    })
                    detected_measurements.add(friendly_body_part_name)
            except requests.ConnectionError:
                pass
    return images


def parse_measurements(measurements):
    parsed_measurements = {}
    parsed_media = []
    if measurements:
        for measurement in measurements:
            measurement_type = measurement.get('measureType', '')
            if measurement_type in VALID_MEASUREMENTS:
                parsed_measurements[measurement_type.lower()] = measurement.get('value')
        parsed_media = get_measurements_pictures(measurements)
    return parsed_measurements, parsed_media
