# Copyright (c) 2019 Deere & Company
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.


import smtplib
from _common_setup import *
from models.FieldOperation import FieldOperation
from models.FieldOperationMeasurement import FieldOpMeasurement
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

font_family_style = "style=\"font-family: Trebuchet MS, Arial, Helvetica, sans-serif; border-collapse: collapse;width:80%;\""
table_data_style = "style=\"border: 1px solid #ddd; padding: 8px; padding-left: 12px;\""
table_row_style_grey = "style=\"background-color: #f2f2f2;\""
table_header_style = "style=\"padding-left: 8px; padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #20730D; color: #ffde00;\""
table_data_and_header_style = "style=\"border: 1px solid #ddd; padding: 8px; padding-left: 12px;padding-left: 8px; padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #20730D; color: #ffde00;\""
should_be_grey = True


def build_send_email(field_name, field_operation: FieldOperation, measurements: FieldOpMeasurement, map_image):
    html_body = build_image_html()
    html_body += build_field_op_html(field_operation, field_name)
    html_body += build_measurement_table_html(measurements)

    body = "<!DOCTYPE html><html><body>" + html_body + "</body></html>";
    send_email(body, map_image)


def send_email(html_body, map_image):
    msg = MIMEMultipart()
    msg["From"] = SEND_FROM
    msg["To"] = ", ".join(SEND_TO)
    msg['Subject'] = EMAIL_SUBJECT

    msg.attach(MIMEText(html_body, 'html'))
    msg.attach(build_email_attachment(map_image))

    with smtplib.SMTP(host=EMAIL_HOST, port=EMAIL_PORT) as server:
        if len(EMAIL_USER) > 0 and len(EMAIL_PW) > 0:
            server.starttls()
            server.login(user=EMAIL_USER, password=EMAIL_PW)

        server.sendmail(from_addr=SEND_FROM, to_addrs=SEND_TO, msg=msg.as_string())


def build_email_attachment(map_image):
    part = MIMEBase('image', 'png')
    m = map_image.split(',')[1]
    part.set_payload(m)
    part.add_header('Content-Transfer-Encoding', 'base64')
    part.add_header("Content-ID", "<mapImage>")
    part['Content-Disposition'] = 'attachment; filename=mapImage'
    return part


def build_image_html():
    return "<h3 style=\"color: #20730D;\">Map Image</h3><img src=\"cid:mapImage\" alt=\"MapImage\" title=\"MapImage\" width=\"250\" height=\"250\"><br>"


def build_field_op_html(fo: FieldOperation, field_name):
    html = build_table("Field Operation Details", 2)
    html += create_table_row("Field Name", field_name)
    html += create_table_row("Type", fo.fieldOperationType)

    if fo.adaptMachineType != "" and fo.adaptMachineType != "unknown":
        html += create_table_row("ADAPT Machine Type", fo.adaptMachineType)

    html += create_table_row("Crop Season", fo.cropSeason)
    html += create_table_row("Start Date", fo.startDate)
    html += create_table_row("End Date", fo.endDate)
    html += "</table><br></p>"

    return html


def build_measurement_table_html(m: FieldOpMeasurement):
    table = build_table("Field Operation Measurement Details", 3)
    table += "<tr><th " + table_data_and_header_style + ">Measurement</th><th " + table_data_and_header_style + ">Value</th><th " + table_data_and_header_style + ">Unit</th></tr>";
    table += create_table_row_with_unit("Name", m.measurementName, "")
    table += create_table_row_with_unit("Category", m.measurementCategory, "")

    if hasattr(m, 'area') and m.area.value > 0:
        table += create_table_row_with_unit("Total Area", m.area.value, m.area.unitId)

    if hasattr(m, 'yield_') and m.yield_.value > 0:
        table += create_table_row_with_unit("Total Yield", m.yield_.value, m.yield_.unitId)

    if hasattr(m, 'averageYield') and m.averageYield.value > 0:
        table += create_table_row_with_unit("Average Yield", m.averageYield.value, m.averageYield.unitId)

    if hasattr(m, 'totalMaterial') and m.totalMaterial.value > 0:
        table += create_table_row_with_unit("Total Material", m.totalMaterial.value, m.totalMaterial.unitId)

    if hasattr(m, 'averageMaterial') and m.averageMaterial.value > 0:
        table += create_table_row_with_unit("Average material", m.averageMaterial.value, m.averageMaterial.unitId)

    if hasattr(m, 'averageMoisture') and m.averageMoisture.value > 0:
        table += create_table_row_with_unit("Average Moisture", m.averageMoisture.value, m.averageMoisture.unitId)

    if hasattr(m, 'averageSpeed') and m.averageSpeed.value > 0:
        table += create_table_row_with_unit("Average Speed", m.averageSpeed.value, m.averageSpeed.unitId)

    table += "</table></p>"
    return table


def build_table(table_name, col_span):
    return "<br><p><table " + font_family_style + "><tr><th colspan=\"" + str(col_span) + "\"" + table_header_style + ">" + table_name + "</th></tr>"


def create_table_row(name, value):
    return "<tr " + get_table_row_style() + "> <td " + table_data_style + ">" + name + "</td><td " + table_data_style + ">" + value + "</td></tr>"


def create_table_row_with_unit(name, value, unit):
    return "<tr " + get_table_row_style() + "> <td " + table_data_style + ">" + name + "</td><td " + table_data_style + ">" + str(value) + "</td><td " + table_data_style + ">" + unit + "</td></tr>"


def get_table_row_style():
    global should_be_grey
    row_style = table_row_style_grey if should_be_grey is True else ""
    should_be_grey = not should_be_grey
    return row_style
