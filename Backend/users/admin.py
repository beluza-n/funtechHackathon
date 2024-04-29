from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'password',
            'first_name', 'last_name',  'middle_name',
            'phone_number', 'telegram', 'job', 'job_title',
            'experience', 'direction', 'image')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class CustomUserAdmin(BaseUserAdmin):
    # form = UserChangeForm
    add_form = UserCreationForm

    model = CustomUser
    list_display = ('email', )
    ordering = ('email',)
    exclude = ('username',)
    fieldsets = (
        ('Personal info', {'fields': (
            'email', 'password',
            'first_name', 'middle_name', 'last_name',
            'phone_number', 'telegram', 'job', 'job_title',
            'experience', 'direction', 'image')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
