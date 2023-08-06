from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib import messages
# from .forms import SignInWithEmailForm

User = get_user_model()


# @admin.register(User)
# class AccountWithEmailAdmin(admin.ModelAdmin):
#     form = SignInWithEmailForm
#     fields = ('email', 'first_name', 'last_name')
#     list_display = ('email', 'is_staff','last_name', 'is_active')
#     ordering = ('-is_staff', 'is_active')
#
#     def save_model(self, request, obj, form, change):
#         obj.save()
#         messages.add_message(
#             request,
#             messages.INFO,
#             'go to your email for account activation'
#         )


# @admin.register(User)
# class AccountWithPhoneAdmin(admin.ModelAdmin):
#     fields = ('phone', 'first_name', 'last_name')
#     list_display = ('phone', 'is_staff','last_name', 'is_active')
#     ordering = ('-is_staff', 'is_active')
#
#     def save_model(self, request, obj, form, change):
#         obj.save()
#         messages.add_message(
#             request,
#             messages.INFO,
#             'go to your phone for account activation'
#         )
