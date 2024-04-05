import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from core.services.jwt_service import ActivateToken, JWTService, PasswordRecoveryToken

# from core.services.jwt_service import ActivateToken, JWTService


class EmailService:
    @staticmethod
    def send_email(to: str, template_name: str, context: dict, subject=''):
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(subject, from_email=os.environ.get('EMAIL_HOST_USER'),
                                     to=[to])

        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    @classmethod
    def register_email(cls, user):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/activate/{token}'
        cls.send_email(user.email, 'register.html', {'name': user.name, 'url': url}, 'Register')

    @classmethod
    def password_recovery(cls, user):
        token = JWTService.create_token(user, PasswordRecoveryToken)
        url = f'http://localhost:3000/recovery-password/{token}'
        cls.send_email(user.email, 'password_recovery.html', {'name': user.name, 'url': url}, 'Password '
                                                                                                      'recovery')
