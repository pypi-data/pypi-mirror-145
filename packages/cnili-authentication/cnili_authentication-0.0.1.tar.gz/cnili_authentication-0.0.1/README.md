# CNILI AUTHENTICATION

## MODULES

Authentication Module that is provided for users with:
- **Email**: Using Email as username_field with otp and reset password functionality.
- **Username**: Using username as username_field, there is no otp or reset password functionality for this type. 
- **Phone**: Same as Email, but you have to Login with otp token all the time.
- **Auth0**: Auth0 is an easy to implement, adaptable authentication and authorization platform.

### AUTH0

for configuring Auth0 in your Project you need to do few steps:

1. You need the following information:
    - Domain: SOCIAL_AUTH_AUTH0_DOMAIN = '*<DOMAIN_NAME>*'
    - Client ID: SOCIAL_AUTH_AUTH0_KEY = '*<AUTH0_KEY>*'
    - Client Secret: SOCIAL_AUTH_AUTH0_SECRET = '*<YOUR_CLIENT_SECRET>*'
2. Configuring Callback Urls
3. Configuring Logout Urls
4. install dependencies in auth0_requirements.txt
5. add 'social_django' to your INSTALLED_APPS
6. add information of  step 1 to your settings with: SOCIAL_AUTH_TRAILING_SLASH = False
7. Set the SOCIAL_AUTH_AUTH0_SCOPE variable with the scopes.

```
SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',
    'profile',
    'email'
]
```

8. Initialize DataBase (migrate).
9. Create the Auth0 Authentication backend.
10. register the authentication backend in settings.
11. Configure the login, redirect login and redirect logout URLs.

if you want to learn more about Auth0, go through the bellow links:

- [Auth0 Docs](https://auth0.com/docs/)
- [Auth0 APIS](https://auth0.com/docs/api)

### Email

Views:
- EmailLoginView
- EnterPasswordView
- EmailAuthenticateView
- ChangePasswordView
- ResetPasswordView
- ResetPasswordVerifyView
- EmailAuthenticateTokenView

Forms:
- EmailSignInForm
- EnterPasswordForm
- ResetPasswordForm

BuiltinForms that has been used in views:
- SetPasswordForm

Urls:
- login/, name=login
- enter-password/, name=enter_password
- authenticate/`<token>`/, name=authenticate
- resend-authenticate-token/, name=resend_authenticate_token
- change-password/, name=change_password
- activate-account/`<token>`/ name=activate_account
- resend-authenticate-account-token/, name=resend_authenticate_account_token
- reset-password/, name=reset_password
- reset-password-verify/`<token>`/, name=reset_password_verify

user fields = {first_name, last_name, email, password, is_staff, is_admin, is_active}

when account will be created, an otp email will be sended to his email for activating account.
also reset_password, change_password is provided for this account

### Phone

Views:
- PhoneLoginView
- EnterLoginCodeView

Forms:
- PhoneSignInForm
- EnterLoginCodeForm

Urls:
- login/, name=login
- enter-login-code/, name=enter_login_code

user fields = {first_name, last_name, phone, password, is_active, is_staff, is_admin}

at first time that user will enter his phone number, we will create an account for him and an otp code will be send for his phone number for login, You must Notice that the users are forced to login with otp code all the time and there is
no password provided for them

you must provide login_with_phone url with one argument for login code:
path('login/<int:code>/', views.LoginView.as_view(), name='login_with_phone')

### Username

Views:
- UsernameLoginView
- UsernameSignUpView

BuiltinForms that has been used in views:
- UserCreationForm
- AuthenticationForm

Urls:
- login/, name=login
- signup/, name=signup
- change-password/, name=change_password

user fields = {first_name, last_name, password, is_active, is_staff, is_admin}

simplest account that has no activation and reset password.

## Using Recaptcha


1. register your site in [recaptcha admin](https://www.google.com/recaptcha/admin/create)
2. add RECAPTCHA_SITE_KEY and RECAPTCHA_SECRET_KEY to your env
3. pip3 install -r requirements/recaptcha_requirements
4. add 'captcha' to INSTALLED_APPS
5. adding captcha form to your forms

```
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class CaptchaForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
```

> This is for recaptcha version2.
