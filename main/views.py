import os
import threading

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings
from django.db.models import Count, Value as V, CharField
from django.db.models.functions import Lower, Concat
from django.contrib import messages

from .models import SessionTypes, Sessions, Tickets, Sales, ExportedReports
from customers.models import Customers
from movies.models import Movies
from staff.models import Staff

from .forms import SessionTypesForm, SessionsForm, \
    TicketsForm, SalesForm
from .utils import export_report


def index(request):
    context = {
        'db_name': settings.DATABASES['default']['NAME'],
        'db_user': settings.DATABASES['default']['USER'],
        'db_host': settings.DATABASES['default']['HOST'],
        'db_port': settings.DATABASES['default']['PORT'],
    }
    return render(request, 'index.html', context)


def session_types(request):
    sort_by = request.GET.get('sort_by', 'session_type_id')
    sort_order = request.GET.get('sort_order', 'asc')

    columns = [
        {'field': 'session_type_id', 'label': 'ID'},
        {'field': 'name', 'label': 'Название'},
    ]
    for col in columns:
        if col['field'] == sort_by:
            col['sort_order'] = 'desc' if sort_order == 'asc' else 'asc'
        else:
            col['sort_order'] = 'asc'

    session_type_list = SessionTypes.objects.all().order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")

    context = {
        'session_types': session_type_list,
        'columns': columns,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }
    return render(request, 'session_types/session_types.html', context)


def session_type_detail(request, session_type_id):
    session_type = get_object_or_404(SessionTypes, session_type_id=session_type_id)
    return render(request, 'session_types/session_type_detail.html', {'session_type': session_type})


def add_session_type(request):
    if request.method == 'POST':
        form = SessionTypesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('session_types')
    else:
        form = SessionTypesForm()
    return render(request, 'add.html', {'form': form})


def edit_session_type(request, session_type_id):
    session_type = get_object_or_404(SessionTypes, session_type_id=session_type_id)
    if request.method == 'POST':
        form = SessionTypesForm(request.POST, instance=session_type)
        if form.is_valid():
            form.save()
            return redirect('session_types')
    else:
        form = SessionTypesForm(instance=session_type)
    return render(request, 'edit.html', {'form': form, 'session_type': session_type})


def delete_session_type(request, session_type_id):
    session_type = get_object_or_404(SessionTypes, session_type_id=session_type_id)
    if request.method == 'POST':
        session_type.delete()
        return redirect('session_types')
    return render(request, 'delete.html', {'redirect_url': reverse('session_types')})


def sessions(request):
    queryset = Sessions.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    session_type = request.GET.get('session_type')
    sort_by = request.GET.get('sort_by', 'session_date')
    sort_order = request.GET.get('sort_order', 'asc')

    if start_date and end_date and start_date > end_date:
        start_date, end_date = end_date, start_date
    if start_date:
        queryset = queryset.filter(session_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(session_date__lte=end_date)
    if session_type:
        queryset = queryset.filter(session_type_id=session_type)

    columns = [
        {'field': 'session_id', 'label': 'ID'},
        {'field': 'session_date', 'label': 'Дата'},
        {'field': 'session_time', 'label': 'Время'},
        {'field': 'session_type__name', 'label': 'Тип сессии'},
        {'field': 'movie__title', 'label': 'Фильм'},
        {'field': 'hall__name', 'label': 'Зал'},
    ]
    for col in columns:
        if col['field'] == sort_by:
            col['sort_order'] = 'desc' if sort_order == 'asc' else 'asc'
        else:
            col['sort_order'] = 'asc'

    queryset = queryset.annotate(
        full_session_type=Concat('session_type__name', V(' '), 'movie__title', output_field=CharField())
    ).order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")

    paginator = Paginator(queryset, 25)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'sessions': page_obj,
        'session_types': SessionTypes.objects.all(),
        'start_date': start_date if start_date is not None else '',
        'end_date': end_date if start_date is not None else '',
        'selected_session_type': int(session_type) if session_type is not None and len(session_type) > 0 else '',
        'columns': columns,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'page_number': page_number,
    }
    return render(request, 'sessions/sessions.html', context)


def session_detail(request, session_id):
    session = get_object_or_404(Sessions, session_id=session_id)
    return render(request, 'sessions/session_detail.html', {'session': session})


def add_session(request):
    if request.method == 'POST':
        form = SessionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sessions')
    else:
        form = SessionsForm()
    return render(request, 'add.html', {'form': form})


def edit_session(request, session_id):
    session = get_object_or_404(Sessions, session_id=session_id)
    if request.method == 'POST':
        form = SessionsForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('sessions')
    else:
        form = SessionsForm(instance=session)
    return render(request, 'edit.html', {'form': form, 'session': session})


def delete_session(request, session_id):
    session = get_object_or_404(Sessions, session_id=session_id)
    if request.method == 'POST':
        session.delete()
        return redirect('sessions')
    return render(request, 'delete.html', {'redirect_url': reverse('sessions')})


def tickets(request):
    queryset = Tickets.objects.all()
    sort_by = request.GET.get('sort_by', 'ticket_id')
    sort_order = request.GET.get('sort_order', 'asc')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price and max_price and float(min_price) > float(max_price):
        min_price, max_price = max_price, min_price
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    if max_price:
        queryset = queryset.filter(price__lte=max_price)

    columns = [
        {'field': 'ticket_id', 'label': 'ID'},
        {'field': 'session', 'label': 'Сеанс'},
        {'field': 'price', 'label': 'Цена'},
        {'field': 'row_number', 'label': 'Ряд'},
        {'field': 'seat_number', 'label': 'Место'},
    ]
    for col in columns:
        if col['field'] == sort_by:
            col['sort_order'] = 'desc' if sort_order == 'asc' else 'asc'
        else:
            col['sort_order'] = 'asc'

    queryset = queryset.order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")

    paginator = Paginator(queryset, 25)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'tickets': page_obj,
        'min_price': min_price if min_price is not None else '',
        'max_price': max_price if max_price is not None else '',
        'columns': columns,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'page_number': page_number,
    }
    return render(request, 'tickets/tickets.html', context)


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Tickets, ticket_id=ticket_id)
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})


def add_ticket(request):
    if request.method == 'POST':
        form = TicketsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tickets')
    else:
        form = TicketsForm()
    return render(request, 'add.html', {'form': form})


def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Tickets, ticket_id=ticket_id)
    if request.method == 'POST':
        form = TicketsForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('tickets')
    else:
        form = TicketsForm(instance=ticket)
    return render(request, 'edit.html', {'form': form, 'ticket': ticket})


def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Tickets, ticket_id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('tickets')
    return render(request, 'delete.html', {'ticket': ticket})


def sales(request):
    queryset = Sales.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    staff = request.GET.get('staff')
    customer = request.GET.get('customer')
    sort_by = request.GET.get('sort_by', 'sale_id')
    sort_order = request.GET.get('sort_order', 'asc')

    if start_date and end_date and start_date > end_date:
        start_date, end_date = end_date, start_date
    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)
    if staff:
        queryset = queryset.filter(staff_id=staff)
    if customer:
        queryset = queryset.filter(customer_id=customer)

    columns = [
        {'field': 'sale_id', 'label': 'ID'},
        {'field': 'ticket', 'label': 'Билет'},
        {'field': 'staff', 'label': 'Сотрудник'},
        {'field': 'date', 'label': 'Дата'},
        {'field': 'payment_type', 'label': 'Тип оплаты'},
        {'field': 'customer', 'label': 'Покупатель'},
    ]
    for col in columns:
        if col['field'] == sort_by:
            col['sort_order'] = 'desc' if sort_order == 'asc' else 'asc'
        else:
            col['sort_order'] = 'asc'

    queryset = queryset.order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")

    paginator = Paginator(queryset, 25)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'sales': page_obj,
        'staffs': Staff.objects.all(),
        'customers': Customers.objects.all(),
        'start_date': start_date if start_date is not None else '',
        'end_date': end_date if end_date is not None else '',
        'selected_staff': int(staff) if staff is not None and len(staff) > 0 else '',
        'selected_customer': int(customer) if customer is not None and len(customer) > 0 else '',
        'columns': columns,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'page_number': page_number,
    }
    return render(request, 'sales/sales.html', context)


def sale_detail(request, sale_id):
    sale = get_object_or_404(Sales, sale_id=sale_id)
    return render(request, 'sales/sale_detail.html', {'sale': sale})


def add_sale(request):
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales')
    else:
        form = SalesForm()
    return render(request, 'add.html', {'form': form})


def edit_sale(request, sale_id):
    sale = get_object_or_404(Sales, sale_id=sale_id)
    if request.method == 'POST':
        form = SalesForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('sales')
    else:
        form = SalesForm(instance=sale)
    return render(request, 'edit.html', {'form': form, 'sale': sale})


def delete_sale(request, sale_id):
    sale = get_object_or_404(Sales, sale_id=sale_id)
    if request.method == 'POST':
        sale.delete()
        return redirect('sales')
    return render(request, 'delete.html', {'sale': sale})


def sales_report(request):
    queryset = Sales.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    staff = request.GET.get('staff')
    customer = request.GET.get('customer')
    sort_by = request.GET.get('sort_by', 'sale_id')
    sort_order = request.GET.get('sort_order', 'asc')

    if start_date and end_date and start_date > end_date:
        start_date, end_date = end_date, start_date
    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)
    if staff:
        queryset = queryset.filter(staff_id=staff)
    if customer:
        queryset = queryset.filter(customer_id=customer)

    columns = [
        {'field': 'sale_id', 'label': 'ID'},
        {'field': 'date', 'label': 'Дата'},
        {'field': 'staff', 'label': 'Сотрудник'},
        {'field': 'customer', 'label': 'Покупатель'},
        {'field': 'ticket__price', 'label': 'Стоимость'},
        {'field': 'ticket__session__session_date', 'label': 'Дата и время сеанса'},
    ]
    for col in columns:
        if col['field'] == sort_by:
            col['sort_order'] = 'desc' if sort_order == 'asc' else 'asc'
        else:
            col['sort_order'] = 'asc'

    queryset = queryset.order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")

    if request.method == 'POST' and 'export_excel' in request.POST:
        def background_task():
            export_report(queryset, 'sales')

        thread = threading.Thread(target=background_task)
        thread.start()
        messages.success(request, 'Экспорт отчета запущен. Детали можно увидеть во вкладке "Экспортированные отчеты"')
        return redirect('report')

    paginator = Paginator(queryset, 25)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'sales': page_obj,
        'staffs': Staff.objects.all(),
        'customers': Customers.objects.all(),
        'start_date': start_date if start_date is not None else '',
        'end_date': end_date if end_date is not None else '',
        'selected_staff': int(staff) if staff is not None and len(staff) > 0 else '',
        'selected_customer': int(customer) if customer is not None and len(customer) > 0 else '',
        'columns': columns,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'page_number': page_number,
    }
    return render(request, 'report/report.html', context)


def staff_report(request):
    queryset = Staff.objects.annotate(
        total_sales=Count('sales')
    ).order_by('-total_sales')

    staff = request.GET.get('staff')
    sort_by = request.GET.get('sort_by', 'staff_id')
    sort_order = request.GET.get('sort_order', 'asc')
    if staff:
        queryset = queryset.filter(staff_id=staff)

    columns = [
        {'field': 'staff_id', 'label': 'ID'},
        {'field': 'first_name', 'label': 'Имя'},
        {'field': 'last_name', 'label': 'Фамилия'},
        {'field': 'middle_name', 'label': 'Отчество'},
        {'field': 'position', 'label': 'Должность'},
        {'field': 'total_sales', 'label': 'Кол-во продаж'},
    ]
    for col in columns:
        if col['field'] == sort_by:
            col['sort_order'] = 'desc' if sort_order == 'asc' else 'asc'
        else:
            col['sort_order'] = 'asc'

    queryset = queryset.order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")

    if request.method == 'POST' and 'export_excel' in request.POST:
        def background_task():
            export_report(queryset, 'staff')

        thread = threading.Thread(target=background_task)
        thread.start()
        messages.success(request, 'Экспорт отчета запущен. Детали можно увидеть во вкладке "Экспортированные отчеты"')
        return redirect('staff-report')

    paginator = Paginator(queryset, 25)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'employees': page_obj,
        'all_staff': Staff.objects.all(),
        'selected_staff': int(staff) if staff is not None and len(staff) > 0 else '',
        'columns': columns,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'page_number': page_number,
    }
    return render(request, 'report/staff_report.html', context)


def movies_report(request):
    queryset = Movies.objects.annotate(
        total_tickets_sold=Count('sessions__tickets')
    ).order_by('-total_tickets_sold')

    movie_id = request.GET.get('movie')
    genre = request.GET.get('genre')
    sort_by = request.GET.get('sort_by', 'movie_id')
    sort_order = request.GET.get('sort_order', 'asc')

    if movie_id:
        queryset = queryset.filter(movie_id=movie_id)
    if genre:
        queryset = queryset.filter(genre=genre)

    columns = [
        {'field': 'movie_id', 'label': 'ID'},
        {'field': 'title', 'label': 'Название'},
        {'field': 'genre', 'label': 'Жанр'},
        {'field': 'duration', 'label': 'Длительность'},
        {'field': 'rating', 'label': 'Рейтинг'},
        {'field': 'total_tickets_sold', 'label': 'Кол-во билетов'},
    ]
    for col in columns:
        if col['field'] == sort_by:
            col['sort_order'] = 'desc' if sort_order == 'asc' else 'asc'
        else:
            col['sort_order'] = 'asc'

    queryset = queryset.order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")

    if request.method == 'POST' and 'export_excel' in request.POST:
        def background_task():
            export_report(queryset, 'movies')

        thread = threading.Thread(target=background_task)
        thread.start()
        messages.success(request, 'Экспорт отчета запущен. Детали можно увидеть во вкладке "Экспортированные отчеты"')

        return redirect('movies-report')

    paginator = Paginator(queryset, 25)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    unique_genres = Movies.objects.order_by(Lower('genre')).values_list('genre', flat=True).distinct()
    context = {
        'movies': page_obj,
        'all_movies': Movies.objects.all(),
        'all_genres': unique_genres,
        'selected_movie': int(movie_id) if movie_id is not None and len(movie_id) > 0 else '',
        'selected_genre': genre if genre is not None and len(genre) > 0 else '',
        'columns': columns,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'page_number': page_number,
    }
    return render(request, 'report/movies_report.html', context)


def exported_reports(request):
    queryset = ExportedReports.objects.all()

    sort_by = request.GET.get('sort_by', '-timestamp')
    sort_order = request.GET.get('sort_order', 'asc')
    columns = [
        {'field': 'timestamp', 'label': 'Дата'},
        {'field': 'report_type', 'label': 'Тип отчета'},
        {'field': 'status', 'label': 'Статус'},
    ]
    for col in columns:
        if col['field'] == sort_by:
            col['sort_order'] = 'desc' if sort_order == 'asc' else 'asc'
        else:
            col['sort_order'] = 'asc'
    queryset = queryset.order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")

    context = {
        'exported_reports': queryset,
        'columns': columns,
        'sort_by': sort_by,
        'sort_order': sort_order
    }
    return render(request, 'report/exported_reports.html', context)


def download_report(request, filename):
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(filepath):
        with open(filepath, 'rb') as fh:
            file_content = fh.read()
            response = HttpResponse(file_content,
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponse("Файл не найден.", status=404)


def get_rows(request):
    session_id = request.GET.get('session_id')
    session = Sessions.objects.get(pk=session_id)
    hall_capacity = session.hall.capacity
    rows = list(range(1, hall_capacity // 20 + 1))

    return JsonResponse({'rows': rows})
