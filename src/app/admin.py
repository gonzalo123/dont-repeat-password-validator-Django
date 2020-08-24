from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import PasswordResetForm
from django.utils.html import format_html
from django.utils.translation import gettext as _

from app.forms import CustomUserCreationForm, CustomUserChangeForm
from app.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff',
                    'is_active']

    add_fieldsets = (
        (None, {
            'description': (
                "Enter the new user's name and email address and click save."
                " The user will be emailed a link allowing them to login to"
                " the site and set their password."
            ),
            'fields': ('username', 'email', 'first_name', 'last_name'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email')}),
        (None, {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        (None, {'fields': ('groups', 'user_permissions')}),
    )

    def send_password_email_to_user(self, request):
        user = CustomUser.objects.get(username=request.POST['username'])
        form = PasswordResetForm({'email': user.email})

        if form.is_valid():
            form.save(
                request=request,
                use_https=False,
                from_email="no-reply@gonzalo123.com",
                email_template_name='registration/password_reset_email_admin.html')

    def response_change(self, request, obj):
        if "_send_email" in request.POST:
            self.send_password_email_to_user(request)
            # handle the action on your obj
            msg = format_html(
                _('Email sent to user with reset password instructions.')
            )
            self.message_user(request, msg, messages.SUCCESS)
            return self.response_post_save_change(request, obj)
        else:
            return super(CustomUserAdmin, self).response_change(request, obj)


admin.site.register(CustomUser, CustomUserAdmin)
