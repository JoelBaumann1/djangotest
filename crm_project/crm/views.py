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
from django.core.mail import send_mass_mail
from django.shortcuts import render, redirect
from .models import Customer
from django.contrib import messages
import requests
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialToken

@login_required
def send_mass_email(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        user = request.user
        token = SocialToken.objects.get(account__user=user, account__provider='microsoft').token
        recipient_list = Customer.objects.values_list('useremail', flat=True)
        for email in recipient_list:
            send_graph_email(token, user.email, email, subject, message)
        # Add your success message and redirect
    # Render your form


def send_graph_email(token, from_email, to_email, subject, body):
    url = 'https://graph.microsoft.com/v1.0/me/sendMail'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {"emailAddress": {"address": to_email}}
            ]
        }
    }
    requests.post(url, headers=headers, json=data)


# def send_mass_email(request):
#     if request.method == 'POST':
#         subject = request.POST['subject']
#         message = request.POST['message']
#         from_email = 'your_ms365_email@example.com'
#         recipient_list = Customer.objects.values_list('useremail', flat=True)
#         messages_to_send = [(subject, message, from_email, [email]) for email in recipient_list]
#         send_mass_mail(messages_to_send, fail_silently=False)
#         messages.success(request, 'Emails sent successfully.')
#         return redirect('customer_list')
#     return render(request, 'crm/send_mass_email.html')

@login_required
def customer_list(request):
    query = request.GET.get('q')
    if query:
        customers = Customer.objects.filter(
            Q(uservorname__icontains=query) | Q(userstatus__icontains=query)
        )
    else:
        customers = Customer.objects.all()
    return render(request, 'crm/customer_list.html', {'customers': customers, 'query': query})

@login_required
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



@login_required
def import_customers_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)

        for row in reader:
            Customer.objects.create(
                userid=row['User ID'],
                uservorname=row['Vorname'],
                userstatus=row['Status']

            )
        messages.success(request, 'CSV file imported successfully.')
        return redirect('customer_list')

    return render(request, 'crm/import_csv.html')
