from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Customers
from .forms import CustomerForm


def customers(request):
    sort_by = request.GET.get('sort_by', 'customer_id')
    sort_order = request.GET.get('sort_order', 'asc')

    columns = [
        {'field': 'customer_id', 'label': 'ID'},
        {'field': 'first_name', 'label': 'Имя'},
        {'field': 'last_name', 'label': 'Фамилия'},
        {'field': 'phone', 'label': 'Телефон'},
        {'field': 'email', 'label': 'Email'},
    ]
    for col in columns:
        if col['field'] == sort_by:
            col['sort_order'] = 'desc' if sort_order == 'asc' else 'asc'
        else:
            col['sort_order'] = 'asc'

    customer_list = Customers.objects.all().order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")
    paginator = Paginator(customer_list, 25)
    page = request.GET.get('page', 1)
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    context = {
        'customers': customers,
        'columns': columns,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'page_number': page,
    }
    return render(request, 'customers/customers.html', context)


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
