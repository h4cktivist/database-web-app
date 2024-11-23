import csv
import threading
from datetime import datetime, timedelta

import openpyxl
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from django.db.models.functions import Concat

from .models import Customers, Halls, Movies, Positions, SessionTypes, Staff, Sessions, Tickets, Sales
from .forms import CustomerForm, HallsForm, MoviesForm, PositionsForm, SessionTypesForm, StaffForm, SessionsForm, TicketsForm, SalesForm


def index(request):
    return render(request, 'index.html')


def customers(request):
    customer_list = Customers.objects.all()
    paginator = Paginator(customer_list, 25)
    page = request.GET.get('page')
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)
    return render(request, 'customers/customers.html', {'customers': customers})


def customer_detail(request, id):
    customer = get_object_or_404(Customers, pk=id)
    return render(request, 'customers/customer_detail.html', {'customer': customer})


def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')
    else:
        form = CustomerForm()
    return render(request, 'add.html', {'form': form})


def edit_customer(request, id):
    customer = get_object_or_404(Customers, pk=id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'edit.html', {'form': form, 'customer': customer})


def delete_customer(request, id):
    customer = get_object_or_404(Customers, pk=id)
    if request.method == 'POST':
        customer.delete()
        return redirect('customers')
    return render(request, 'delete.html', {'redirect_url': reverse('customers')})


def halls(request):
    hall_list = Halls.objects.all().order_by('hall_id')
    return render(request, 'halls/halls.html', {'halls': hall_list})


def hall_detail(request, id):
    hall = get_object_or_404(Halls, pk=id)
    return render(request, 'halls/hall_detail.html', {'hall': hall})


def add_hall(request):
    if request.method == 'POST':
        form = HallsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('halls')
    else:
        form = HallsForm()
    return render(request, 'add.html', {'form': form})


def edit_hall(request, id):
    hall = get_object_or_404(Halls, pk=id)
    if request.method == 'POST':
        form = HallsForm(request.POST, instance=hall)
        if form.is_valid():
            form.save()
            return redirect('halls')
    else:
        form = HallsForm(instance=hall)
    return render(request, 'edit.html', {'form': form, 'hall': hall})


def delete_hall(request, id):
    hall = get_object_or_404(Halls, pk=id)
    if request.method == 'POST':
        hall.delete()
        return redirect('halls')
    return render(request, 'delete.html', {'redirect_url': reverse('halls')})


def movies(request):
    movie_list = Movies.objects.all()
    paginator = Paginator(movie_list, 25)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    return render(request, 'movies/movies.html', {'movies': movies})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movies, movie_id=movie_id)
    return render(request, 'movies/movie_detail.html', {'movie': movie})


def add_movie(request):
    if request.method == 'POST':
        form = MoviesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies')
    else:
        form = MoviesForm()
    return render(request, 'add.html', {'form': form})


def edit_movie(request, movie_id):
    movie = get_object_or_404(Movies, movie_id=movie_id)
    if request.method == 'POST':
        form = MoviesForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies')
    else:
        form = MoviesForm(instance=movie)
    return render(request, 'edit.html', {'form': form, 'movie': movie})


def delete_movie(request, movie_id):
    movie = get_object_or_404(Movies, movie_id=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('movies')
    return render(request, 'delete.html', {'redirect_url': reverse('movies')})


def positions(request):
    position_list = Positions.objects.all()
    return render(request, 'positions/positions.html', {'positions': position_list})


def position_detail(request, position_id):
    position = get_object_or_404(Positions, position_id=position_id)
    return render(request, 'positions/position_detail.html', {'position': position})


def add_position(request):
    if request.method == 'POST':
        form = PositionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('positions')
    else:
        form = PositionsForm()
    return render(request, 'add.html', {'form': form})


def edit_position(request, position_id):
    position = get_object_or_404(Positions, position_id=position_id)
    if request.method == 'POST':
        form = PositionsForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            return redirect('positions')
    else:
        form = PositionsForm(instance=position)
    return render(request, 'edit.html', {'form': form, 'position': position})


def delete_position(request, position_id):
    position = get_object_or_404(Positions, position_id=position_id)
    if request.method == 'POST':
        position.delete()
        return redirect('positions')
    return render(request, 'delete.html', {'redirect_url': reverse('positions')})


def session_types(request):
    session_type_list = SessionTypes.objects.all()
    return render(request, 'session_types/session_types.html', {'session_types': session_type_list})


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


def staff(request):
    staff_list = Staff.objects.all()
    paginator = Paginator(staff_list, 25)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    return render(request, 'staff/staff.html', {'staff': page_obj})


def staff_detail(request, staff_id):
    staff_member = get_object_or_404(Staff, staff_id=staff_id)
    return render(request, 'staff/staff_detail.html', {'staff': staff_member})


def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff')
    else:
        form = StaffForm()
    return render(request, 'add.html', {'form': form})


def edit_staff(request, staff_id):
    staff_member = get_object_or_404(Staff, staff_id=staff_id)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff_member)
        if form.is_valid():
            form.save()
            return redirect('staff')
    else:
        form = StaffForm(instance=staff_member)
    return render(request, 'edit.html', {'form': form, 'staff_member': staff_member})


def delete_staff(request, staff_id):
    staff_member = get_object_or_404(Staff, staff_id=staff_id)
    if request.method == 'POST':
        staff_member.delete()
        return redirect('staff')
    return render(request, 'delete.html', {'redirect_url': reverse('staff')})


def sessions(request):
    queryset = Sessions.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    session_type = request.GET.get('session_type')

    if start_date:
        queryset = queryset.filter(session_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(session_date__lte=end_date)
    if session_type:
        queryset = queryset.filter(session_type_id=session_type)

    paginator = Paginator(queryset, 25)  # Пагинация применяется к отфильтрованному queryset
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
        'start_date': start_date,
        'end_date': end_date,
        'session_type': session_type,
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
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    if max_price:
        queryset = queryset.filter(price__lte=max_price)

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
        'min_price': min_price,
        'max_price': max_price
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

    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)
    if staff:
        queryset = queryset.filter(staff_id=staff)
    if customer:
        queryset = queryset.filter(customer_id=customer)

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
        'start_date': start_date,
        'end_date': end_date,
        'staff': staff,
        'customer': customer,
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


def report(request):
    queryset = Sales.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    staff = request.GET.get('staff')
    customer = request.GET.get('customer')

    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)
    if staff:
        queryset = queryset.filter(staff_id=staff)
    if customer:
        queryset = queryset.filter(customer_id=customer)

    if request.method == 'POST' and 'export_excel' in request.POST:
        return export_to_excel(queryset)

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
        'start_date': start_date,
        'end_date': end_date,
        'staff': staff,
        'customer': customer,
    }
    return render(request, 'report/report.html', context)


def export_to_excel(queryset):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append([
        'ID', 'Дата', 'Сотрудник', 'Покупатель', 'Стоимость', 'Дата и время сеанса'
    ])
    for sale in queryset:
        staff_name = f"{sale.staff.first_name} {sale.staff.last_name}"  # Adjust as needed
        customer_name = f"{sale.customer.first_name} {sale.customer.last_name}" # Adjust as needed
        session_datetime = f"{sale.ticket.session.session_date} {sale.ticket.session.session_time}"
        sheet.append([
            sale.sale_id, sale.date, staff_name, customer_name, sale.ticket.price, session_datetime  # Add other relevant fields
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sales_report.xlsx"'
    workbook.save(response)
    return response
