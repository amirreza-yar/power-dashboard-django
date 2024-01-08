# serializers.py
import csv
from django.http import StreamingHttpResponse
from rest_framework.renderers import BaseRenderer

class CSVRenderer(BaseRenderer):
    media_type = 'text/csv'
    format = 'csv'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, list):
            csv_data = self.list_to_csv(data)
        else:
            csv_data = self.object_to_csv(data)
        
        response = StreamingHttpResponse(
            (csv_data),
            content_type='text/csv',
        )
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        return response

    def list_to_csv(self, data):
        buffer = StringIO()
        writer = csv.writer(buffer)

        # Write headers
        writer.writerow(data[0].keys())

        # Write data
        for item in data:
            writer.writerow(item.values())
        
        buffer.seek(0)
        return buffer

    def object_to_csv(self, data):
        buffer = StringIO()
        writer = csv.writer(buffer)

        # Write headers
        writer.writerow(data.keys())

        # Write data
        writer.writerow(data.values())

        buffer.seek(0)
        return buffer
