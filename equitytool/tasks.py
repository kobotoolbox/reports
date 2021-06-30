import datetime
import re
import zipfile
from io import BytesIO, StringIO

import huey.signals
from django.db import transaction
from django.core import management
from django.core.files.base import ContentFile
from huey.contrib import djhuey


@djhuey.db_task()
def generate_admin_stats(report_task_pk):
    """ Generates zipped CSV about user activity for administrators """
    from .models import AdminStatsReportTask

    REPORTS = {
        'users.csv': {'args': {'user_report': True}},
        'projects.csv': {'args': {'project_report': True}},
    }
    with transaction.atomic():
        report_task = AdminStatsReportTask.objects.select_for_update().get(
            pk=report_task_pk
        )
        if report_task.status != report_task.NEW:
            raise RuntimeError(
                f'Report task {report_task_pk} has already started'
            )
        report_task.status = report_task.PENDING
        report_task.save(update_fields=['status'])
        with BytesIO() as output_file:
            with zipfile.ZipFile(
                output_file, 'w', zipfile.ZIP_DEFLATED
            ) as zip_file:
                for filename, report_settings in REPORTS.items():
                    with StringIO() as csv_io:
                        management.call_command(
                            'print_stats',
                            stdout=csv_io,
                            **report_settings['args'],
                        )
                        zip_file.writestr(filename, csv_io.getvalue())
            output_file.seek(0)
            report_task.result.save(
                'equitytool_admin_stats_{}.zip'.format(datetime.datetime.now()),
                ContentFile(output_file.read()),
            )

        report_task.status = report_task.COMPLETE
        report_task.save()
        return str(report_task)


@djhuey.signal(huey.signals.SIGNAL_ERROR)
def mark_task_as_failed(signal, huey_task, exc=None):
    from .models import AdminStatsReportTask

    # this is an okay assumption because there's only one task defined
    report_task_pk = huey_task.args[0]
    with transaction.atomic():
        report_task = AdminStatsReportTask.objects.select_for_update().get(
            pk=report_task_pk
        )
        if report_task.status != report_task.COMPLETE:
            report_task.status = report_task.FAILED
            report_task.save(update_fields=['status'])
