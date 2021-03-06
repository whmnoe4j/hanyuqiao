from django.contrib import admin
from appuser.models import MyUser,MyUserToken
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from appuser.models import MyUser,MyUserToken

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('cellphone',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
       

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('cellphone','is_superuser','is_admin','admin_type')
    list_filter = ('is_admin',)
    readonly_fields=('pubdate',)
    fieldsets = (
        (None, {'fields': ('cellphone','password')}),
        ('Personal info', {'fields': ('cname','nick','email','cell','pic','tel','city','zipcode','abroad','country','language','f_l','education','degree','gender',
                                      'birthday','born_place','university','career','religion','blood','star','zod','inte','desc','point','hanbi','level',
                                      'pubdate','installdate','favorites',)}),

        ('Permissions', {'fields': (('is_admin','admin_type'),'is_superuser',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cellphone', 'password1', 'password2',('is_admin','admin_type'),'is_superuser',)}
        ),
    )
    ordering=('id',)
    search_fields = ['cellphone','cname','email',]
    filter_horizontal = ('favorites',)


admin.site.register(MyUser, MyUserAdmin)
admin.site.unregister(Group)
admin.site.register(MyUserToken)
