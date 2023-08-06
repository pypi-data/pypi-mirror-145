import pdfkit
from django.template import Context, Template, TemplateSyntaxError


def _prepare_headers(headers):
    result = []
    for header in list(headers):
        result.append(header.replace('_', ' '))
    return result


def _generate_pdf(report_title, headers_set, data, pdf_html_template):
    rows_per_table = 23

    if len(data) > rows_per_table:
        table_data = []
        first_index = 0
        while first_index < len(data):
            table_data.append(data[first_index:first_index + rows_per_table])
            first_index = first_index + rows_per_table
    else:
        table_data = [data]
    context = {
        'report_title': report_title.replace('_', ' '),
        'table_data': table_data,
        'headers': _prepare_headers(headers_set),
        'records_count': len(data)
    }
    try:
        rendered_ticket = Template(
            pdf_html_template()
        ).render(
            Context(context)
        )
    except TemplateSyntaxError as e:
        raise e

    options = {
        'orientation': 'Landscape',
        'page-width': '216',
        'page-height': '279'
    }
    return pdfkit.from_string(rendered_ticket, output_path=False, options=options)


def _get_pdf_html_template():
    return "<!DOCTYPE html>\
                <html>\
                <head>\
                <style>\
                table {\
                  font-family: arial, sans-serif;\
                  border-collapse: collapse;\
                  width: 100%;\
                }\
                td, th {\
                  border: 1px solid #DDDDDD;\
                  text-align: left;\
                  padding: 8px;\
                }\
                div.page {\
                    width: 380mm;\
                    overflow: hidden;\
                    page-break-before: always;\
                }\
                tr:nth-child(even) {\
                  background-color: #DDDDDD;\
                }\
                </style>\
                </head>\
                <body>\
                    {% for data in table_data %}\
                        <h2>{{report_title}}</h2>\
                        <table>\
                            <tr>\
                                {% for header in headers %}\
                                    <th style=\"text-align: center; font-weight: bold; background-color: #5a0000; color: white\">"\
                                        "{{header}}"\
                                    "</th>\
                                {% endfor %}\
                            </tr>\
                            {% for row in data %}\
                                <tr style=\"height: 16px !important; font-size: 11px;\">\
                                    {% for field in row %}\
                                        <td style=\"" \
                                            "text-align: center;" \
                                            "white-space: nowrap;" \
                                            "overflow: hidden;" \
                                            "text-overflow: ellipsis;" \
                                            "height: 16px !important;" \
                                            "font-weight: bold;" \
                                            "font-size: 11px;"\
                                            "\">{{ row|get_item:field }}</td>\
                                   {% endfor %}\
                                </tr>\
                            {% endfor %}\
                        </table>\
                        <div class=\"page\">\
                        </div>\
                    {% endfor %}\
                    <div style=\"text-align: center; font-weight: bold; background-color: #5a0000; color: white\">" \
                       "Rendered first 500 records." \
                    "</div>\
                    <br>\
                    {% if records_count > 0 %}\
                        <div style=\"text-align: center; font-weight: bold; background-color: #5a0000; color: white\">" \
                            "All records number: {{records_count}}." \
                       "</div>\
                    {% endif %}\
                </body>\
            </html>"
