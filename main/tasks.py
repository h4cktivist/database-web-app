from celery import shared_task

from .utils import export_report


@shared_task(bind=True)
def export_report_task(self, queryset, report_type):
    file_path = export_report(queryset, report_type)
    if file_path:
        return {'file_path': file_path, 'report_type': report_type, 'task_id': self.request.id}
    else:
        return {'error': 'Ошибка при генерации отчета'}
