from django.shortcuts import render, get_object_or_404, redirect, reverse

from .models import Halls
from .forms import HallsForm


def halls(request):
    sort_by = request.GET.get('sort_by', 'hall_id')
    sort_order = request.GET.get('sort_order', 'asc')

    columns = [
        {'field': 'hall_id', 'label': 'ID'},
        {'field': 'name', 'label': 'Название'},
        {'field': 'capacity', 'label': 'Вместимость'},
    ]
    for col in columns:
        if col['field'] == sort_by:
            col['sort_order'] = 'desc' if sort_order == 'asc' else 'asc'
        else:
            col['sort_order'] = 'asc'

    hall_list = Halls.objects.all().order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")

    context = {
        'halls': hall_list,
        'columns': columns,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }
    return render(request, 'halls/halls.html', context)


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

