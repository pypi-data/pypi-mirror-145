from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import View, FormView
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import SetPasswordForm

from .commons.redis import Redis
from .forms import EnterLoginCodeForm, PhoneSignInForm, ResetPasswordForm

User = get_user_model()


# Global Views

class ChangePassword:
    # TODO
    pass


# Email Views

class EmailLoginView:
    # TODO
    pass


class EnterPasswordView:
    # TODO
    pass


class EmailAuthenticateView:
    # TODO
    pass


class ChangePasswordView:
    # TODO
    pass


class EmailAccountActivationView(View):
    """
    get user base on token and activate that user
    """
    success_url = None

    def get(self, request, token):
        email = Redis().get_activation_email(token).decode('utf-8')
        user = get_object_or_404(User, email=email)
        user.is_active = True
        user.save()
        return render(request, self.success_url)


class PasswordResetView(FormView):
    """
    take email from user and send a reset password view to email.
    main operation handeled in form.save() method
    """
    form_class = ResetPasswordForm
    template_name = 'form.html'
    success_url = reverse_lazy('auth_app:hello')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ResetPasswordVerifyView(FormView):
    """
    get email from redis with token key
    set new password for user with that email
    """
    template_name = None
    form_class = SetPasswordForm
    success_url = None

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        email = Redis().get_reset_email(self.kwargs.get('token')).decode('utf-8')
        user = get_object_or_404(User, email=email)
        kwargs.update({'user': user})
        return kwargs


# Phone Views

class LoginWithPhoneView(FormView):
    """
    take user phone and otp token will be sended to user
    phone via sms in form.save() method
    """
    template_name = None
    form_class = PhoneSignInForm
    success_url = None

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EnterLoginCodeView(FormView):
    """
    get code that sended via sms to user phone if code is not expired
    and is true, user with that phone number will be logined
    """
    template_name = None
    form_class = EnterLoginCodeForm
    success_url = None

    def form_valid(self, form):
        phone = Redis().get_otp_phone(form.cleaned_data.get('code')).decode('utf-8')
        user = get_object_or_404(User, phone=phone)
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)


# Username Views

class UsernameSignUpView:
    # TODO
    pass
