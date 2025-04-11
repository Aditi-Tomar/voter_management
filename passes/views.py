from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from .forms import PassRequestForm
from .models import PassRequest
from xhtml2pdf import pisa
import io


def request_pass_form(request):
    if request.method == 'POST':
        form = PassRequestForm(request.POST)
        if form.is_valid():
            # Save the pass request
            pass_request = form.save()

            # Send confirmation email
            send_confirmation_email(pass_request)

            messages.success(request,
                             "Thank you for reaching out! We've received your form and will get back to you shortly.")
            return redirect('passes:request_pass_form')
    else:
        form = PassRequestForm()

    context = {
        'form': form,
        'temple_choices': PassRequest.TEMPLE_CHOICES,
        'min_date': timezone.now().date(),
    }
    return render(request, 'passes/request_form.html', context)


def send_confirmation_email(pass_request):
    subject = 'Temple Pass Request Received'
    message = render_to_string('passes/approval_email.html', {
        'pass_request': pass_request,
        'is_confirmation': True
    })

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [pass_request.email],
        fail_silently=False,
        html_message=message
    )


def send_status_email(pass_request):
    if pass_request.status == 'ACCEPTED':
        subject = 'Temple Pass Request Approved'
        template = 'passes/approval_email.html'

        # Generate PDF
        pdf_content = generate_pass_pdf(pass_request)

        # Create email
        email = EmailMessage(
            subject,
            render_to_string(template, {
                'pass_request': pass_request,
                'is_accepted': True
            }),
            settings.DEFAULT_FROM_EMAIL,
            [pass_request.email]
        )

        # Attach PDF
        email.attach(f'temple_pass_{pass_request.id}.pdf', pdf_content, 'application/pdf')
        email.send()

    elif pass_request.status == 'REJECTED':
        subject = 'Temple Pass Request Rejected'
        template = 'passes/rejection_email.html'

        message = render_to_string(template, {'pass_request': pass_request})

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [pass_request.email],
            fail_silently=False,
            html_message=message
        )


def generate_pass_pdf(pass_request):
    template = get_template('passes/pass_template.html')
    html = template.render({'pass_request': pass_request})

    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        return result.getvalue()
    return None