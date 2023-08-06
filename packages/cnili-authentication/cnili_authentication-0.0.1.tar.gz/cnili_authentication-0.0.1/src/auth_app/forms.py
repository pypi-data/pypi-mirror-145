from django import forms
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from commons.redis import Redis
from commons.utils import MOBILE_NUMBER_VALIDATOR

User = get_user_model()


# Recaptcha form
class ReCaptchaV2FiledMixin:
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


# forms for EmailAccount

class EmailForm(forms.Form):
    email = forms.EmailField()


class SignInWithEmailForm(EmailForm):

    def save(self, **kwargs):
        user = super().save(commit=kwargs.get('commit'))
        if not user.password:
            user.set_otp()
        return user


class EnterPasswordForm(forms.Form):
    password = forms.CharField(
        label=_('password'),
        max_length=40, 
        widget=forms.PasswordInput()
        )


class ResetPasswordForm(EmailForm):
    def save(self):
        user = get_object_or_404(User, email=self.clean().get('email'))
        user.send_reset_password()
        return user

# using SetPasswordForm for setting password
# using PasswordChangeForm for changing password

# forms for UsernameAccount

# using UserCreationForm for User Creation
# using AuthenticationForm for authentication form


# forms for PhoneAccount

class PhoneForm(forms.Form):
    phone = forms.CharField(
        label=_('phone'),
        max_length=15,
        validators=[MOBILE_NUMBER_VALIDATOR]
    )


class PhoneSignInForm(PhoneForm):
    """
    send otp token to user with phone
    """
    def save(self):
        user = User.objects.get_or_create(phone=self.clean().get('phone'))
        user.send_otp()
        return user


class EnterLoginCodeForm(forms.Form):
    """
    Check for code existence in redis
    """
    code = forms.IntegerField(
        label=_('Login Code')
    )

    def is_valid(self) -> bool:
        valid = super().is_valid()
        if valid:
            phone = Redis().get_otp_phone(self.cleaned_data.get('code'))
            if phone:
                return True
        return False
