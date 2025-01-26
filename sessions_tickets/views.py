from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Value as V, CharField
from django.db.models.functions import Concat
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import SessionTypes, Sessions, Tickets
from .forms import SessionTypesForm, SessionsForm, TicketsForm


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
