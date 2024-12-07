import os
import openpyxl
from django.http import FileResponse, HttpResponse
from docx import Document
from docx.enum.section import WD_ORIENT

from django.utils.timezone import now
from django.conf import settings

from .models import ExportedReports


def make_record(report_type, status=0, report_id=None, filepath=None):
    if status == 0:
        record = ExportedReports(
            report_type=report_type,
            status=status,
        )
        record.save()
        return record.report_id

    else:
        record = ExportedReports.objects.get(report_id=report_id)
        record.status = status
        record.word_filepath = f'{filepath}.docx'
        record.excel_filepath = f'{filepath}.xlsx'
        record.save()


def export_report(queryset, report_type):
    record_id = make_record(report_type)

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    doc = Document()
    section = doc.sections[0]
    section.orientation = WD_ORIENT.LANDSCAPE
    new_width, new_height = section.page_height, section.page_width
    section.page_width = new_width
    section.page_height = new_height

    if report_type == 'sales':
        columns = [
            'ID', 'Дата', 'Сотрудник', 'Покупатель', 'Стоимость', 'Дата и время сеанса'
        ]
        sheet.append(columns)

        doc.add_heading('Отчет по продажам', 0)
        table = doc.add_table(rows=1, cols=len(columns))
        hdr_cells = table.rows[0].cells
        for i, column_name in enumerate(columns):
            hdr_cells[i].text = column_name

        for sale in queryset:
            staff_name = f"{sale.staff.first_name} {sale.staff.last_name}"
            customer_name = f"{sale.customer.first_name} {sale.customer.last_name}"
            session_datetime = f"{sale.ticket.session.session_date} {sale.ticket.session.session_time}"

            sheet.append([
                sale.sale_id, sale.date, staff_name, customer_name, sale.ticket.price, session_datetime
            ])
            row_cells = table.add_row().cells
            for i, cell_data in enumerate([sale.sale_id, sale.date, staff_name, customer_name, sale.ticket.price, session_datetime]):
                row_cells[i].text = str(cell_data)

        filename = f"sales_report_{now().strftime('%Y%m%d_%H%M%S')}"

    elif report_type == 'staff':
        columns = ['ID', 'Имя', 'Фамилия', 'Отчество', 'Должность', 'Кол-во продаж']
        sheet.append(columns)

        doc.add_heading('Отчет по сотрудникам', 0)

        table = doc.add_table(rows=1, cols=len(columns))
        hdr_cells = table.rows[0].cells
        for i, column_name in enumerate(columns):
            hdr_cells[i].text = column_name

        for staff in queryset:
            if staff.position is None:
                data = [
                    staff.staff_id, staff.first_name, staff.last_name, staff.middle_name, None, staff.total_sales
                ]

            else:
                data = [
                    staff.staff_id, staff.first_name, staff.last_name, staff.middle_name, staff.position.title, staff.total_sales
                ]

            sheet.append(data)
            row_cells = table.add_row().cells
            for i, cell_data in enumerate(data):
                row_cells[i].text = str(cell_data)

        filename = f"staff_report_{now().strftime('%Y%m%d_%H%M%S')}"

    elif report_type == 'movies':
        columns = ['ID', 'Название', 'Жанр', 'Длительность', 'Рейтинг', 'Кол-во билетов']
        sheet.append(columns)

        doc.add_heading('Отчет по фильмам', 0)
        table = doc.add_table(rows=1, cols=len(columns))
        hdr_cells = table.rows[0].cells
        for i, column_name in enumerate(columns):
            hdr_cells[i].text = column_name

        for movie in queryset:
            data = [
                movie.movie_id, movie.title, movie.genre, movie.duration, movie.rating,
                movie.total_tickets_sold
            ]
            sheet.append(data)
            row_cells = table.add_row().cells
            for i, cell_data in enumerate(
                    [movie.movie_id, movie.title, movie.genre, movie.duration, movie.rating, movie.total_tickets_sold]):
                row_cells[i].text = str(cell_data)

        filename = f"movies_report_{now().strftime('%Y%m%d_%H%M%S')}"

    filepath = os.path.join(settings.MEDIA_ROOT, 'reports', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    workbook.save(f'{filepath}.xlsx')
    doc.save(f'{filepath}.docx')

    make_record(report_type, status=1, report_id=record_id, filepath=filepath)
