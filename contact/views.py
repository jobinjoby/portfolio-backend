from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ContactMessage

@api_view(['POST'])
def contact_submit(request):
    data = request.data

    # Save to database
    msg = ContactMessage.objects.create(
        name=data.get('name'),
        email=data.get('email'),
        subject=data.get('subject'),
        message=data.get('message'),
    )

    # Send email notification to YOU
    send_mail(
        subject=f"New Contact From Portfolio: {msg.subject}",
        message=f"""
Someone contacted you from your portfolio!

Name: {msg.name}
Email: {msg.email}
Subject: {msg.subject}

Message:
{msg.message}
        """,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.NOTIFICATION_EMAIL],
        fail_silently=False,   # ← This shows errors if email fails
    )

    return Response({'status': 'success', 'message': 'Message sent!'})