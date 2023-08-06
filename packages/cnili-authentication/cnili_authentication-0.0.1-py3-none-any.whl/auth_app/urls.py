from django.urls import path
from django.contrib.auth import get_user_model

from . import views
# from .models import EmailAccount, UsernameAccount, PhoneAccount
from .models import EmailAccount
User = get_user_model()

app_name = 'auth_app'
urlpatterns = []

if User(issubclass(User, EmailAccount)):
    urlpatterns += [
        # account activation
        path('login/', views.EmailLoginView.as_view(), name='login'),
        path('authenticate/<token>/', views.EmailAuthenticateTokenView.as_view(), name='authenticate_token'),
        path('enter-password/<email>/', views.EnterPasswordView.as_view(), name='enter_password'),
        # reset_password
        path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
        path('password-reset-verify/<token>/', views.ResetPasswordVerifyView.as_view(), name='password_reset_verify'),
    ]

# if User(issubclass(User, PhoneAccount)):
#     urlpatterns += [
#         path('login/', views.LoginWithPhoneView.as_view(), name='login'),
#         path('enter-login-code/', views.EnterLoginCodeView.as_view(), name='enter_login_code'),
#     ]
#
#
# if User(issubclass(User, UsernameAccount)):
#     # TODO
#     pass

# # Auth0 Urls
# urlpatterns += [
#     path('', include('social_django.urls')),
# ]
