from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PassRequest
from .serializers import PassRequestSerializer
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


@api_view(['POST'])
def submit_pass_request(request):
    serializer = PassRequestSerializer(data=request.data)
    if serializer.is_valid():
        pass_request = serializer.save()
        # Send confirmation email
        send_confirmation_email(pass_request)
        return Response({
            'message': "Thank you for reaching out! We've received your form and will get back to you shortly.",
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_request_status(request, request_id):
    pass_request = get_object_or_404(PassRequest, id=request_id)
    new_status = request.data.get('status')

    if new_status not in ['ACCEPTED', 'REJECTED']:
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    pass_request.status = new_status
    pass_request.save()

    # Send status notification email
    if new_status == 'ACCEPTED':
        send_acceptance_email(pass_request)
    else:
        send_rejection_email(pass_request)

    return Response({'message': f'Request {new_status.lower()}'})


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


def send_acceptance_email(pass_request):
    subject = 'Temple Pass Request Approved'
    message = render_to_string('passes/approval_email.html', {
        'pass_request': pass_request,
        'is_accepted': True
    })
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [pass_request.email],
        fail_silently=False,
        html_message=message
    )


def send_rejection_email(pass_request):
    subject = 'Temple Pass Request Rejected'
    message = render_to_string('passes/rejection_email.html', {
        'pass_request': pass_request
    })
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [pass_request.email],
        fail_silently=False,
        html_message=message
    )