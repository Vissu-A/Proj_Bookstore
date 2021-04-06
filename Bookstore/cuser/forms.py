from django import forms
from datetime import datetime

from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm, UserCreationForm, AuthenticationForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.forms.widgets import Widget
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from cuser.models import User


class AdminUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
        required=True # Default is True
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
        required=True # Default is True
    )

    # phone regex with country separation ====>  ^\+\d{1,4}[-]{1}?\d{8,11}$
    # phone regex with out country separation =====>  ^\+\d{9,15}$ (or) ^\+\d{1,4}?\d{8,11}$
    phone_regex = RegexValidator(regex=r'^\+\d{1,4}?\d{8,11}$', message="Phone number must be entered in the format: '+919999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(
        label='Phone number', 
        widget=forms.NumberInput(attrs={'class':'form-control', 'type':'tel', 'placeholder':'+Country Number (+919999999999)'}),
        strip=False,
        help_text="<ul><li>Phone number must be numeric.</li><li>Please enter phone number including country code. Ex: +919999999999.</li></ul>", 
        required=True, # Default is True
        validators=[phone_regex],
        max_length=17,
    )

    class Meta:
        model = User
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class AdminUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField( 
        label="Password",
        help_text=
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"{}\">this form</a>."
        ,
    )

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = self.fields['password'].help_text.format('../password/')
        f = self.fields.get('user_permissions')
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CustomUserRegistrationForm(forms.ModelForm):
   
    """
    A form that creates a user, with no privileges, from the given username and
    password. This custom registration form is implimented by copying the Default 
    UserRegistrationForm logic. Because applying class attribute in the widgets on password
    fields of subclass extended the UserRegistrationForm like above commented from is 
    not working.
    """
    
    error_messages = {
        'password_mismatch': ('The two passcode fields didn’t match.'),
    }
    
    password1 = forms.CharField(
        label=("Passcode"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'true'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    
    password2 = forms.CharField(
        label=("Passcode confirmation"),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'true'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

    # phone regex with country separation ====>  ^\+\d{1,4}[-]{1}?\d{8,11}$
    # phone regex with out country separation =====>  ^\+\d{9,15}$ (or) ^\+\d{1,4}?\d{8,11}$
    phone_regex = RegexValidator(regex=r'^\+\d{1,4}?\d{8,11}$', message="Phone number must be entered in the format: '+919999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(
        label='Phone number', 
        widget=forms.NumberInput(attrs={'class':'form-control', 'type':'tel', 'placeholder':'+Country Number (+919999999999)'}),
        strip=False,
        help_text="<ul><li>Phone number must be numeric.</li><li>Please enter phone number including country code. Ex: +919999999999.</li></ul>", 
        required=True, # Default is True
        validators=[phone_regex],
        max_length=17,
    )
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone']
        
        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control', 'autofocus':True}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Example@email.com'}),
        }

        labels = {
            'email' : 'Email address',
        }
        
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)
                
    
    def clean_email(self):
        '''
        This function is used to clean the email field of registrationform.
        it check wether email is alreday taken or not.
        '''

        print('clean email method entered.')
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email = email).exists():
            self.add_error('email', 'Email already taken!')
        return email
                
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class Loginform(forms.Form):
    email = forms.EmailField(
        max_length = 255, 
        label = 'Email', 
        widget = forms.TextInput(attrs={'class':'form-control', 'autofocus':True})
    )
    passcode = forms.CharField(
        label = 'Passcode',
        strip = False,
        widget = forms.PasswordInput(attrs={'class':'form-control'})
    )
    
    
class CustomResetPasswordFrom(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password.
    this is implimented based on the default SetPasswordForm from class.
    """ 
    
    error_messages = {
        'password_mismatch': ('The two password fields didn’t match.'),
    }   
    
    new_passcode1 = forms.CharField(
        label=("New passcode"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_passcode2 = forms.CharField(
        label=("Confirm"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}),
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_new_passcode2(self):
        password1 = self.cleaned_data.get('new_passcode1')
        password2 = self.cleaned_data.get('new_passcode2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_passcode1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class CustomUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'date_of_birth', 'gender']
        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control', 'autofocus':True, 'readonly':True}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'readonly':True}),
            'phone': forms.NumberInput(attrs={'class':'form-control', 'type':'tel', 'readonly':True}),
            'date_of_birth': forms.DateInput(attrs={'class':'form-control', 'type':'date', 'readonly':True}),
            'gender': forms.TextInput(attrs={'class':'form-control', 'readonly':True})
        }


class CustomUserChangeForm(forms.ModelForm):

    # phone regex with country separation ====>  ^\+\d{1,4}[-]{1}?\d{8,11}$
    # phone regex with out country separation =====>  ^\+\d{9,15}$ (or) ^\+\d{1,4}?\d{8,11}$
    phone_regex = RegexValidator(regex=r'^\+\d{1,4}?\d{8,11}$', message="Phone number must be entered in the format: '+919999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(
        label='Phone number', 
        widget=forms.NumberInput(attrs={'class':'form-control', 'type':'tel', 'placeholder':'+Country Number (+919999999999)'}),
        strip=False,
        help_text="<ul><li>Phone number must be numeric.</li><li>Please enter phone number including country code. Ex: +919999999999.</li></ul>", 
        required=False, # Default is True
        validators=[phone_regex],
        max_length=17,
    )

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'date_of_birth', 'gender', 'img']
        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control', 'autofocus':True}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'gender': forms.Select(attrs={'class':'form-control'}),
            'img': forms.FileInput(attrs={'class':'form-control', 'type':'hidden'}),
        }
        labels = {
            'img':'',
        }


class CustomPasswordResestMailForm(PasswordResetForm):
    email = forms.EmailField(
        label = 'Email',
        widget = forms.EmailInput(attrs={'class':'form-control', 'autofocus':True}),
    )

class CustomPasswordChangeForm(forms.Form):

    error_messages = {
        'password_incorrect': _("Your old password was entered incorrectly."),
        'password_mismatch': _('The two password fields didn’t match.'),
    }

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password', 'autofocus': True}),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self) -> str:
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )

        return old_password
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class CustomSetPasswordForm(forms.Form):

    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }

    password1 = forms.CharField(
        label = 'New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autofocus': True}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label = 'Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data['password1']
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

