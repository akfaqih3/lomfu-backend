from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.urls import reverse
from decouple import config
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from .models import UserRole

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    Group.objects.get_or_create(name=UserRole.TEACHER)
    Group.objects.get_or_create(name=UserRole.STUDENT)



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    """
    print("====================================")
    context = {
        'current_user': reset_password_token.user,
        'name': reset_password_token.user.name,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # Render email messages (both plain text and HTML)
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    # Create the email object and send
    msg = EmailMultiAlternatives(
        subject="Password Reset for {title}".format(title=config('APP_NAME')),
        body=email_plaintext_message,
        from_email=config('DEFAULT_FROM_EMAIL'),
        to=[reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
