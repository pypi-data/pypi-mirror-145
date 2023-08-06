from collections import OrderedDict
from dataclasses import dataclass

import io
import csv
from io import BytesIO
import xlsxwriter
import pytz
from django.core.files.base import ContentFile
from django.db.models import QuerySet
from rest_framework.fields import IntegerField

from reports.pdf_generator import _get_pdf_html_template, _generate_pdf
from reports.report_serializers import BaseReportSerializer
from serializers import AmountField


@dataclass
class DateTimeMetaData:
    custom_timezone: pytz.BaseTzInfo
    datetime_format: str
    date_format: str


@dataclass
class ReportMetaData:
    report_title: str
    queryset: QuerySet
    serializer_class: BaseReportSerializer
    headers_set: list
    summary_fields: list


class FileFormat:
    PDF = 'pdf'
    XLSX = 'xls'
    CSV = 'csv'


class ReportFileService:
    DEFAULT_TIMEZONE = pytz.timezone('UTC')
    DEFAULT_DATE_TIME_FORMAT = '%m/%d/%Y %I:%M %p'
    DEFAULT_DATA_FORMAT = '%m/%d/%Y'

    def __init__(self, report_meta_data: ReportMetaData, data_time_meta_data: DateTimeMetaData = None):
        self.report_title = report_meta_data.report_title
        self.queryset = report_meta_data.queryset

        self._set_report_meta_data(report_meta_data)
        self.data_time_meta_data = self._get_data_time_meta_data(data_time_meta_data)

        self.data = self._create_data()

    def generate_pdf(self) -> ContentFile:
        headers_set = self.headers_set[:12]
        pdf = _generate_pdf(self.report_title, headers_set, self.data, self._get_pdf_html_template())
        return ContentFile(pdf)

    def generate_excel(self) -> ContentFile:
        buffer = BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, self.headers_set)
        worksheet_row = 1
        for row in self.data:
            worksheet.write_row(worksheet_row, 0, row.values())
            worksheet_row += 1
        workbook.close()
        buffer.seek(0)
        return ContentFile(buffer.read())

    def generate_csv(self) -> ContentFile:
        output = io.StringIO()
        writer = csv.writer(
            output,
            quoting=csv.QUOTE_NONE,
            delimiter=',',
            quotechar=None,
            escapechar="\\"
        )
        writer.writerow(self.headers_set)
        for row in self.data:
            writer.writerow(row.values())
        output.seek(0)
        return ContentFile(output.read().encode('utf-8'))

    def _set_report_meta_data(self, report_meta_data):
        self.headers_set = report_meta_data.headers_set is not None if report_meta_data.headers_set \
            else report_meta_data.serializer_class.Meta.fields
        self.summary_fields = report_meta_data.summary_fields is not None if report_meta_data.summary_fields else []

        class _Serializer(report_meta_data.serializer_class):
            class Meta(report_meta_data.serializer_class.Meta):
                fields = self.headers_set

        self.serializer_class = _Serializer

    def _get_data_time_meta_data(self, data_time_meta_data):
        if not data_time_meta_data:
            return DateTimeMetaData(
                self.DEFAULT_TIMEZONE, self.DEFAULT_DATE_TIME_FORMAT, self.DEFAULT_DATA_FORMAT
            )
        if not data_time_meta_data.custom_timezone:
            data_time_meta_data.custom_timezone = self.DEFAULT_TIMEZONE
        if not data_time_meta_data.datetime_format:
            data_time_meta_data.datetime_format = self.DEFAULT_DATE_TIME_FORMAT
        if not data_time_meta_data.date_format:
            data_time_meta_data.date_format = self.DEFAULT_DATA_FORMAT
        return data_time_meta_data

    def _create_data(self):
        template_serializer = self.serializer_class(
            self.queryset, many=True, custom_timezone=self.data_time_meta_data.custom_timezone,
            datetime_format=self.data_time_meta_data.datetime_format,
            date_format=self.data_time_meta_data.date_format,
        )
        data = template_serializer.data
        self._create_summary(data)
        return data

    @staticmethod
    def _get_pdf_html_template():
        return _get_pdf_html_template()

    def _create_summary(self, data):
        if len(data) == 0:
            return
        summary_dict = {}
        for key in data[0]:
            summary_dict[key] = 0

        for column in self.summary_fields:
            for row in data:
                value = row[column]
                if value is not None:
                    if isinstance(row[column], str):
                        value = float(value)
                    summary_dict[column] += value
            if isinstance(summary_dict[column], float):
                summary_dict[column] = AmountField().to_representation(value=summary_dict[column])
            else:
                summary_dict[column] = str(IntegerField().to_representation(value=summary_dict[column]))

        for key in summary_dict:
            if summary_dict[key] == 0:
                summary_dict[key] = '--'

        if summary_dict:
            data.append(OrderedDict(summary_dict))
        return data
