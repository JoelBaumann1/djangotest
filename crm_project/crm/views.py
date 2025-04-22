from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Customer
from django.db.models import Q
import csv
from django.http import HttpResponse
from .models import Customer
from django.shortcuts import redirect
from django.contrib import messages


def customer_list(request):
    query = request.GET.get('q')
    if query:
        customers = Customer.objects.filter(
            Q(uservorname__icontains=query) | Q(userstatus__icontains=query)
        )
    else:
        customers = Customer.objects.all()
    return render(request, 'crm/customer_list.html', {'customers': customers, 'query': query})


def export_customers_csv(request):
    query = request.GET.get('q', '')
    customers = Customer.objects.all()

    if query:
        customers = customers.filter(uservorname__icontains=query)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_customers.csv"'

    writer = csv.writer(response)
    writer.writerow(['User ID', 'Vorname', 'Status'])

    for customer in customers:
        writer.writerow([customer.userid, customer.uservorname, customer.userstatus])

    return response




def import_customers_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)

        for row in reader:
            Customer.objects.create(
                userid=row['User ID'],
                uservorname=row['Vorname'],
                userstatus=row['Status'],
            )
        messages.success(request, 'CSV file imported successfully.')
        return redirect('customer_list')

    return render(request, 'crm/import_csv.html')
