# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from bookmanagement.tasks import generate_report
from django.conf import settings
import os
import json

class ReportViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        reports_dir = settings.REPORTS_DIR
        if not os.path.exists(reports_dir):
            return Response({"detail": "No reports stored"}, status=status.HTTP_404_NOT_FOUND)

        report_files = sorted(
            [f for f in os.listdir(reports_dir) if f.endswith('.json')],
            reverse=True
        )

        if report_files:
            with open(os.path.join(reports_dir, report_files[0]), 'r') as f:
                report_data = json.load(f)
            return Response(report_data, status=status.HTTP_200_OK)
        return Response({"detail": "No reports found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Trigger background task to generate report
        generate_report.delay()
        return Response({"detail": "Report generation started"}, status=status.HTTP_202_ACCEPTED)
