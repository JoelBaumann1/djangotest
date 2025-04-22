from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Customer
from django.db.models import Q

def customer_list(request):
    query = request.GET.get('q')
    if query:
        customers = Customer.objects.filter(
            Q(uservorname__icontains=query) | Q(userstatus__icontains=query)
        )
    else:
        customers = Customer.objects.all()
    return render(request, 'crm/customer_list.html', {'customers': customers, 'query': query})
