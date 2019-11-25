# Copyright (c) 2019 Deere & Company
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.


from models.Event import Event
import fieldop_service
import json
from _demo_helper import DemoHelper

demo_helper = DemoHelper()


def lambda_handler(event, context):
    demo_helper.setup()
    demo_helper.logger.info(event['body'])
    field_operation_links = get_field_op_links(event['body'])
    if len(field_operation_links) > 0:
        fieldop_service.process_links(field_operation_links)

    return {
        "isBase64Encoded": False,
        "statusCode": 204,
        "headers": {"ContentType": "application/json"},
        "body": "{\"my\": \"response\"}",
    }


def get_field_op_links(event):
    events = json.loads(event)
    urls = []
    for item in events:
        event = Event(item)
        if event.eventTypeId == "fieldOperation":
            urls.append(event.targetResource)

    return urls


