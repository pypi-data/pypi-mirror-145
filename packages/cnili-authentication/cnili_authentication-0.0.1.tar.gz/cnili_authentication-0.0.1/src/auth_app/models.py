from decouple import config
import secrets

from django.urls.base import reverse_lazy
from django.utils import timezone
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from commons.kavenegar import KavenegarAPI

from commons.utils import MOBILE_NUMBER_VALIDATOR
from .managers import UserManagerWithUsername, UserManagerWithPhone, UserManagerWithEmail
from commons.redis import Redis


class CustomBaseUser(AbstractBaseUser, PermissionsMixin):
    """
    An Abstract base class implementing a basic featured User model with
    admin-compliant permissions.

    if you want to use it you must inheritance it and complete missed fields.
    """

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    class Meta:
        verbose_name = _('Custom user')
        verbose_name_plural = _('Custom users')
        abstract = True

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def make_password(self):
        if not self.password:
            password = self.objects.make_random_password(length=14)
            self.set_password(password)
            return password
        return False

    def send_reset_password(self):
        pass

    def send_otp(self):
        pass
    
    
class EmailAccount(CustomBaseUser):
    email = models.EmailField(
        verbose_name=_('email address'),
        unique=True,
        error_messages={
            'unique': _('An account with that email already exist.')
        }
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManagerWithEmail()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def send_reset_password(self) -> None:
        subject = 'Reset Password'
        token = secrets.token_urlsafe(16)  # generate 16 char token
        Redis().set_reset_token(token, self.email)
        url = reverse_lazy('auth_app:password_reset_verify', kwargs={'token': token})
        message = f'reset password link:\n http://localhost:8000{url}'
        send_mail(
            subject=subject,
            message=message,
            recipient_list=[self.email],
            from_email=config('EMAIL_HOST_USER'),
        )

    def send_otp(self):
        subject = 'Login'
        token = secrets.token_urlsafe(16)  # generate 16 char token
        Redis().set_otp_token(token, self.email)
        url = reverse_lazy('auth_app:authenticate_token', kwargs={'token': token})
        message = f'Login link:\n http://localhost:8000{url}'
        status = send_mail(
            subject=subject,
            message=message,
            recipient_list=[self.email],
            from_email=config('EMAIL_HOST_USER'),
        )
        return status

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
        

# class UsernameAccount(CustomBaseUser):
#     """
#     An Account that uses Username as username_field.
#
#     Notice that this account can't use Account_Activation and Reset_Password
#     or other similar actions inside it unless add an email_field to it and
#     add your own methods to perform those actions
#     """
#     username_validator = UnicodeUsernameValidator()
#
#     username = models.CharField(
#         verbose_name=_('username'),
#         max_length=150,
#         unique=True,
#         help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#         validators=[username_validator],
#         error_messages={
#             'unique': _("A user with that username already exists."),
#         },
#     )
#
#     objects = UserManagerWithUsername()
#
#     # EMAIL_FIELD = None
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = []
#
#     @property
#     def __str__(self):
#         return self.username
#
#
# class PhoneAccount(CustomBaseUser):
#     """
#     An Account That use Phone as username_field.
#
#     this account doesn't use password, and each time it uses
#     the otp token for authentication
#     """
#     _kavenegar = None
#
#     phone = models.CharField(
#         verbose_name=_('Phone'),
#         max_length=15,
#         validators=[MOBILE_NUMBER_VALIDATOR],
#         unique=True,
#         help_text=_('Required. 15 characters. digits only.'),
#         error_messages={
#             'unique': _("A user with that phone already exists."),
#         },
#     )
#
#     objects = UserManagerWithPhone()
#
#     EMAIL_FIELD = 'phone'
#     USERNAME_FIELD = 'phone'
#     REQUIRED_FIELDS = []
#
#     @classmethod
#     def _get_kavenegar(cls):
#         if not cls._kavenegar:
#             cls._kavenegar = KavenegarAPI(
#                 config('KAVENEGAR_API_KET'),
#                 timeout=int(config('KAVENEGAR_TIMEOUT'))
#             )
#         return cls._kavenegar
#
#     def __str__(self):
#         return self.phone
#
#     def send_sms(self, **kwargs):
#         api = self._get_kavenegar()
#         params = {
#             'receptor': self.phone,  # multiple mobile number, split by comma
#             'message': kwargs.get('message'),
#             'sender': kwargs.get('sender'),  # optional
#         }
#         api.sms_send(params)
#
#     def send_otp(self):
#         token = secrets.randbits(20)  # generate int with 20 random bits
#         Redis().set_otp_code(token, self.phone)  # set token in redis
#         message = f'Your Login token: {token}'
#         self.send_sms(message=message)
