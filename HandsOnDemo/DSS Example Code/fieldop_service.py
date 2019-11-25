# Copyright (c) 2019 Deere & Company
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.


import email_service
from models.FieldOperationMeasurement import FieldOpMeasurement
from models.FieldOperation import FieldOperation
import json
from _demo_helper import DemoHelper

demo_helper = DemoHelper()


def process_links(events):
    demo_helper.setup()
    for e in events:
        field_operation = get_object(e, FieldOperation)

        measurement_type = None

        if "seed" in field_operation.fieldOperationType:
            measurement_type = "seedingRateResult"
        elif "harvest" in field_operation.fieldOperationType:
            measurement_type = "harvestYieldResult"

        if measurement_type is None:
            demo_helper.logger.info('Field operation type: ' + field_operation.fieldOperationType + ' not found. Please update code!')
            return

        demo_helper.logger.info('measurement type set as: ' + measurement_type)
        field_name = get_field_name(field_operation)

        measurement_url = search_links_for_url(field_operation.links, measurement_type)
        measurements = get_object(measurement_url, FieldOpMeasurement)

        map_image_url = search_links_for_url(measurements.links, "mapImage")
        map_image = get_image_string(map_image_url)

        email_service.build_send_email(field_name, field_operation, measurements, map_image)


def search_links_for_url(links, search_value):
    for l in links:
        if l['rel'] == search_value:
            return l['uri']


def get_field_name(field_operation: FieldOperation):
    field_link = search_links_for_url(field_operation.links, 'field')
    response = demo_helper.get_from_url_link(field_link)
    return response['name']


def get_object(url, cls):
    response = demo_helper.get_from_url_link(url)
    return cls(json.dumps(response))


def get_image_string(url):
    response = demo_helper.get_from_url_link_with_image(url)
    return response['value']['image']
