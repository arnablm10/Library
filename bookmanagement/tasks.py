

import json
import os
from django.utils.timezone import now
from django.conf import settings
from celery import shared_task
import logging
from bookmanagement.models import Author, Book, BorrowRecord

logger = logging.getLogger(__name__)
# Task to generate the report
@shared_task
def generate_report():
    timestamp = now().strftime('%Y%m%d')

    total_authors = Author.objects.count()
    total_books = Book.objects.count()
    total_borrowed_books = BorrowRecord.objects.filter(return_date__isnull=True).count()

    report_data = {
        "total_authors": total_authors,
        "total_books": total_books,
        "total_borrowed_books": total_borrowed_books,
    }

    # Define the file path where the report will be saved
    report_dir = settings.REPORTS_DIR
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    report_filename = f'report_{timestamp}.json'
    report_file_path = os.path.join(report_dir, report_filename)

    # Save the report as a JSON file
    with open(report_file_path, 'w') as report_file:
        json.dump(report_data, report_file)

    return f'Report generated: {report_filename}'