from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Positions, Staff
from .forms import PositionsForm, StaffForm


def positions(request):
    sort_by = request.GET.get('sort_by', 'position_id')
    sort_order = request.GET.get('sort_order', 'asc')

    columns = [
        {'field': 'position_id', 'label': 'ID'},
        {'field': 'title', 'label': 'Название'},
    ]
    for col in columns:
        if col['field'] == sort_by:
            col['sort_order'] = 'desc' if sort_order == 'asc' else 'asc'
        else:
            col['sort_order'] = 'asc'

    position_list = Positions.objects.all().order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")

    context = {
        'positions': position_list,
        'columns': columns,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }
    return render(request, 'positions/positions.html', context)


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



def staff(request):
    sort_by = request.GET.get('sort_by', 'staff_id')
    sort_order = request.GET.get('sort_order', 'asc')

    columns = [
        {'field': 'staff_id', 'label': 'ID'},
        {'field': 'first_name', 'label': 'ФИО'},
        {'field': 'position', 'label': 'Должность'},
        {'field': 'phone', 'label': 'Телефон'},
    ]
    for col in columns:
        if col['field'] == sort_by:
            col['sort_order'] = 'desc' if sort_order == 'asc' else 'asc'
        else:
            col['sort_order'] = 'asc'

    staff_list = Staff.objects.all().order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")
    paginator = Paginator(staff_list, 25)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'staff': page_obj,
        'columns': columns,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'page_number': int(page_number)
    }
    return render(request, 'staff/staff.html', context)


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
