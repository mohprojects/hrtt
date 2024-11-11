from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.validators import (
    EmailValidator,
    MaxLengthValidator,
    MinLengthValidator,
    # ValidationError,
    validate_email,
    validate_integer,
)
from app.models.organizations import Organizations

from app.models.users import Users
from app.validators import IsPhoneNumberValidator


class UserSignInForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email Id",
        min_length=5,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(5), MaxLengthValidator(100), EmailValidator],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "style": "font-weight:bold",
                "placeholder": "",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        min_length=8,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(8), MaxLengthValidator(100)],
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "style": "font-weight:bold",
                "placeholder": "",
            }
        ),
    )

    def clean_email(self):
        data = self.cleaned_data["email"]
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address")
        try:
            user = Users.objects.get(user_username=data)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            user = None
        if user is None:
            raise forms.ValidationError('Email Id: "%s" is not yet registered.' % data)
        else:
            return data

    def clean_password(self):
        password = self.cleaned_data["password"]
        # check for min length
        min_length = 8
        if len(password) < min_length:
            msg = "Password must be at least %s characters long." % (str(min_length))
            self.add_error("password", msg)
        # check for digit
        if sum(c.isdigit() for c in password) < 1:
            msg = "Password must contain at least 1 number."
            self.add_error("password", msg)
        # check for uppercase letter
        if not any(c.isupper() for c in password):
            msg = "Password must contain at least 1 uppercase letter."
            self.add_error("password", msg)
        # check for lowercase letter
        if not any(c.islower() for c in password):
            msg = "Password must contain at least 1 lowercase letter."
            self.add_error("password", msg)
        return password

    class Meta:
        model = Users
        fields = (
            "email",
            "password",
        )


class UserSignInCaptchaForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email Id",
        min_length=5,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(5), MaxLengthValidator(100), EmailValidator],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "style": "font-weight:bold",
                "placeholder": "",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        min_length=8,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(8), MaxLengthValidator(100)],
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "style": "font-weight:bold",
                "placeholder": "",
            }
        ),
    )

    # captcha = ReCaptchaField(
    #     widget=ReCaptchaV2Checkbox(
    #         attrs={
    #             "data-theme": "light",
    #             "data-size": "normal",
    #         }
    #     )
    # )

    def clean_email(self):
        data = self.cleaned_data["email"]
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address")
        try:
            user = Users.objects.get(user_username=data)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            user = None
        if user is None:
            raise forms.ValidationError('Email Id: "%s" is not yet registered.' % data)
        else:
            return data

    def clean_password(self):
        password = self.cleaned_data["password"]
        # check for min length
        min_length = 8
        if len(password) < min_length:
            msg = "Password must be at least %s characters long." % (str(min_length))
            self.add_error("password", msg)
        # check for digit
        if sum(c.isdigit() for c in password) < 1:
            msg = "Password must contain at least 1 number."
            self.add_error("password", msg)
        # check for uppercase letter
        if not any(c.isupper() for c in password):
            msg = "Password must contain at least 1 uppercase letter."
            self.add_error("password", msg)
        # check for lowercase letter
        if not any(c.islower() for c in password):
            msg = "Password must contain at least 1 lowercase letter."
            self.add_error("password", msg)
        return password

    class Meta:
        model = Users
        fields = (
            "email",
            "password",
        )


class UserForgotPasswordForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email Id",
        min_length=5,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(5), MaxLengthValidator(100), EmailValidator],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "style": "font-weight:bold",
                "placeholder": "",
            }
        ),
    )

    # captcha = ReCaptchaField(
    #     required=False,
    #     # attrs={
    #     #     'theme': 'clean',
    #     #     'style': 'width:100%',
    #     # }
    # )

    def clean_email(self):
        data = self.cleaned_data["email"]
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address")
        try:
            user = Users.objects.get(user_username=data)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            user = None
        if user is None:
            raise forms.ValidationError('Email Id: "%s" is not yet registered.' % data)
        else:
            return data

    class Meta:
        model = Users
        fields = ("email",)


class UserResetPasswordForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email Id",
        min_length=5,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(5), MaxLengthValidator(100), EmailValidator],
        disabled=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "style": "font-weight:bold",
                "placeholder": "",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        min_length=8,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(8), MaxLengthValidator(100)],
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "style": "font-weight:bold",
                "placeholder": "",
            }
        ),
    )
    repeat_password = forms.CharField(
        label="Repeat password",
        min_length=8,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(8), MaxLengthValidator(100)],
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "style": "font-weight:bold",
                "placeholder": "",
            }
        ),
    )

    def clean_email(self):
        data = self.cleaned_data["email"]
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address")
        return data

    def clean_password(self):
        password = self.cleaned_data["password"]
        # check for min length
        min_length = 8
        if len(password) < min_length:
            msg = "Password must be at least %s characters long." % (str(min_length))
            self.add_error("password", msg)
        # check for digit
        if sum(c.isdigit() for c in password) < 1:
            msg = "Password must contain at least 1 number."
            self.add_error("password", msg)
        # check for uppercase letter
        if not any(c.isupper() for c in password):
            msg = "Password must contain at least 1 uppercase letter."
            self.add_error("password", msg)
        # check for lowercase letter
        if not any(c.islower() for c in password):
            msg = "Password must contain at least 1 lowercase letter."
            self.add_error("password", msg)
        return password

    def clean(self):
        cleaned_data = super(UserResetPasswordForm, self).clean()

        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")
        if password and repeat_password:
            if password != repeat_password:
                msg = "Password doesn't match."
                self.add_error("repeat_password", msg)
        return cleaned_data

    class Meta:
        model = Users
        fields = (
            "email",
            "password",
            "repeat_password",
        )


class UserSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(UserSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Users
        fields = ()


class UserCreateForm(forms.ModelForm):
    first_name = forms.CharField(
        label="First Name",
        min_length=3,
        max_length=50,
        required=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    middle_name = forms.CharField(
        label="Middle Name",
        min_length=3,
        max_length=50,
        required=False,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        min_length=3,
        max_length=50,
        required=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )

    phone_number = forms.CharField(
        label="Phone Number",
        min_length=9,
        max_length=15,
        validators=[
            MinLengthValidator(9),
            MaxLengthValidator(15),
            IsPhoneNumberValidator,
        ],
        required=True,
        widget=forms.TextInput(
            attrs={
               "type": "tel",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ))
    
    email = forms.EmailField(
        label="Email Id",
        min_length=5,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(5), MaxLengthValidator(100), EmailValidator],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        min_length=8,
        max_length=100,
        required=False,
        validators=[MinLengthValidator(8), MaxLengthValidator(100)],
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    repeat_password = forms.CharField(
        label="Repeat password",
        min_length=8,
        max_length=100,
        required=False,
        validators=[MinLengthValidator(8), MaxLengthValidator(100)],
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    role = forms.ChoiceField(
        choices=Users.ARRAY_ROLES,
        initial="",
        label="Role",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-role",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    organization_id = forms.ChoiceField(
        choices= (('', '--select--'),),
        initial='',
        label='Organization',
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-organization-id",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ))

    def clean_name(self):
        data = self.cleaned_data["name"]
        return data

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        #try:
        #     validate_integer(data)
        # except ValidationError:
        #     raise forms.ValidationError("Enter a valid phone number")
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address")

        try:
            user = Users.objects.get(user_username=data)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            user = None
        if user is not None:
            raise forms.ValidationError('Email Id: "%s" is already in use.' % data)
        return data

    def clean_password(self):
        password = self.cleaned_data["password"]
        # # check for min length
        # min_length = 8
        # if len(password) < min_length:
        #     msg = "Password must be at least %s characters long." % (str(min_length))
        #     self.add_error("password", msg)
        # # check for digit
        # if sum(c.isdigit() for c in password) < 1:
        #     msg = "Password must contain at least 1 number."
        #     self.add_error("password", msg)
        # # check for uppercase letter
        # if not any(c.isupper() for c in password):
        #     msg = "Password must contain at least 1 uppercase letter."
        #     self.add_error("password", msg)
        # # check for lowercase letter
        # if not any(c.islower() for c in password):
        #     msg = "Password must contain at least 1 lowercase letter."
        #     self.add_error("password", msg)
        return password

    def clean_role(self):
        data = self.cleaned_data["role"]
        return data

    def clean_organization_id(self):
        data = self.cleaned_data["organization_id"]
        return data
    
    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        return data

    def clean_middle_name(self):
        data = self.cleaned_data["middle_name"]
        return data

    def clean_last_name(self):
        data = self.cleaned_data["last_name"]
        return data

    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()

        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")
        if password and repeat_password:
            if password != repeat_password:
                msg = "Password doesn't match."
                self.add_error("repeat_password", msg)
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(UserCreateForm, self).__init__(*args, **kwargs)

        ORGANIZATIONS = (('', '--select--'),)
        organizations = Organizations.objects.all()
        if user.user_role == Users.TYPE_ACTIVITY_MANAGER:
            organizations = Organizations.objects.filter(organization_id = user.organization_id)
            self.fields['role'] = forms.ChoiceField(
                choices=((Users.TYPE_DATA_REPORTER, 'DATA REPORTER'),),
                initial="",
                label="Role",
                required=True,
                validators=[],
                widget=forms.Select(
                    attrs={
                        "id": "search-input-select-role",
                        "class": "form-control",
                        "style": "width:100%;",
                        "placeholder": "",
                    }
                ),
            )

        for item in organizations:
            ORGANIZATIONS = ORGANIZATIONS + \
                ((item.organization_id, item.organization_name),)
        self.fields['organization_id'] = forms.ChoiceField(
            choices=ORGANIZATIONS,
            label='Organization',
            required=True,
            validators=[],
            widget=forms.Select(
                attrs={
                    'id': 'search-input-select-organization-id',
                    'class': 'form-control',
                    "style": "font-weight:bold",
                    'style': 'width:100%;',
                    'placeholder': '--select--',
                }
            )) 

    class Meta:
        model = Users
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            'phone_number',
            'email',
            'password',
            'repeat_password',
            'role',
            'organization_id',
        )


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email Id",
        min_length=5,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(5), MaxLengthValidator(100), EmailValidator],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ))

    first_name = forms.CharField(
        label="First Name",
        min_length=3,
        max_length=50,
        required=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    middle_name = forms.CharField(
        label="Middle Name",
        min_length=3,
        max_length=50,
        required=False,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        min_length=3,
        max_length=50,
        required=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )

    phone_number = forms.CharField(
        label="Phone Number",
        min_length=9,
        max_length=15,
        validators=[
            MinLengthValidator(9),
            MaxLengthValidator(15),
            IsPhoneNumberValidator,
        ],
        required=True,
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    role = forms.ChoiceField(
        choices=Users.ARRAY_ROLES,
        initial="",
        label="Role",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-role",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    organization_id = forms.ChoiceField(
        choices=(
            ('', '--select--'),
        ),
        initial="",
        label="Organization",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-organization-id",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ))

    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        return data

    def clean_middle_name(self):
        data = self.cleaned_data["middle_name"]
        return data

    def clean_last_name(self):
        data = self.cleaned_data["last_name"]
        return data

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        try:
            validate_integer(data)
        except ValidationError:
            raise forms.ValidationError("Enter a valid phone number")
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address")
        try:
            user = Users.objects.get(user_username=data)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            user = None
        if user is None:
            raise forms.ValidationError('Email Id: "%s" does not exist.' % data)
        else:
            return data

    def clean_role(self):
        data = self.cleaned_data["role"]
        return data

    def clean_organization_id(self):
        data = self.cleaned_data["organization_id"]
        return data

    def clean(self):
        cleaned_data = super(UserUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        ORGANIZATIONS = (('', '--select--'),)
        organizations = Organizations.objects.all()
        if user.user_role == Users.TYPE_ACTIVITY_MANAGER:
            organizations = Organizations.objects.filter(organization_id = user.organization_id)
        for item in organizations:
            ORGANIZATIONS = ORGANIZATIONS + \
                ((item.organization_id, item.organization_name),)
        
        self.fields['organization_id'] = forms.ChoiceField(
            choices=ORGANIZATIONS[1:],
            label='Organization',
            required=True,
            validators=[],
            widget=forms.Select(
                attrs={
                    'id': 'search-input-select-organization-id',
                    'class': 'form-control',
                    "style": "font-weight:bold",
                    'style': 'width:100%;',
                    'placeholder': '--select--',
                }
            )) 

    class Meta:
        model = Users
        fields = (
            'email',
            "first_name",
            "middle_name",
            "last_name",
            'phone_number',
            'role',
            'organization_id',
        )


class UserViewForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email Id",
        min_length=5,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(5), MaxLengthValidator(100), EmailValidator],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ))
    
    first_name = forms.CharField(
        label="First Name",
        min_length=3,
        max_length=50,
        required=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    middle_name = forms.CharField(
        label="Middle Name",
        min_length=3,
        max_length=50,
        required=False,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        min_length=3,
        max_length=50,
        required=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    phone_number = forms.CharField(
        label="Phone Number",
        min_length=9,
        max_length=15,
        validators=[
            MinLengthValidator(9),
            MaxLengthValidator(15),
            IsPhoneNumberValidator,
        ],
        required=True,
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    role = forms.ChoiceField(
        choices=Users.ARRAY_ROLES,
        initial="",
        label="Role",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-role",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    organization_id = forms.ChoiceField(
        choices=(
            ('', '--select--'),),
        initial='',
        label='Organization',
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-organization-id",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ))

    def clean_name(self):
        data = self.cleaned_data["name"]
        # try:
        # except ValidationError:
        #     raise forms.ValidationError('Enter a valid name')
        return data

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        # try:
        #     validate_integer(data)
        # except ValidationError:
        #     raise forms.ValidationError("Enter a valid phone number")
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address")
        try:
            user = Users.objects.get(user_username=data)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            user = None
        if user is None:
            raise forms.ValidationError('Email Id: "%s" does not exist.' % data)
        else:
            return data

    def clean_role(self):
        data = self.cleaned_data["role"]
        return data

    def clean_organization_id(self):
        data = self.cleaned_data["organization_id"]
        return data

    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        return data

    def clean_middle_name(self):
        data = self.cleaned_data["middle_name"]
        return data

    def clean_last_name(self):
        data = self.cleaned_data["last_name"]
        return data

    def clean(self):
        cleaned_data = super(UserUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(UserViewForm, self).__init__(*args, **kwargs)

        ORGANIZATIONS = (('', '--select--'),)
        organizations = Organizations.objects.all()
        if user.user_role == Users.TYPE_ACTIVITY_MANAGER:
            organizations = Organizations.objects.filter(organization_id = user.organization_id)
        for item in organizations:
            ORGANIZATIONS = ORGANIZATIONS + (
                (item.organization_id, item.organization_name),
            )
        self.fields["organization_id"] = forms.ChoiceField(
            choices=ORGANIZATIONS,
            initial="",
            label="Organization",
            required=True,
            validators=[],
            widget=forms.Select(
                attrs={
                    "id": "search-input-select-organization-id",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "--select--",
                    "readonly": True,
                    "disabled": True,
                }
            ),
        )

    class Meta:
        model = Users
        fields = (
            'email',
            "first_name",
            "middle_name",
            "last_name",
            'phone_number',
            'role',
            'organization_id',
        )


class UserProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email Id",
        min_length=5,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(5), MaxLengthValidator(100), EmailValidator],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ))

    first_name = forms.CharField(
        label="First Name",
        min_length=3,
        max_length=50,
        required=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    middle_name = forms.CharField(
        label="Middle Name",
        min_length=3,
        max_length=50,
        required=False,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        min_length=3,
        max_length=50,
        required=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )

    phone_number = forms.CharField(
        label="Phone Number",
        min_length=9,
        max_length=15,
        validators=[
            MinLengthValidator(9),
            MaxLengthValidator(15),
            IsPhoneNumberValidator,
        ],
        required=True,
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    def clean_name(self):
        data = self.cleaned_data["name"]
        # try:
        # except ValidationError:
        #     raise forms.ValidationError('Enter a valid name')
        return data

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        # try:
        #     validate_integer(data)
        # except ValidationError:
        #     raise forms.ValidationError("Enter a valid phone number")
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address")
        try:
            user = Users.objects.get(user_username=data)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            user = None
        if user is None:
            raise forms.ValidationError('Email Id: "%s" does not exist.' % data)
        else:
            return data
    
    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        return data

    def clean_middle_name(self):
        data = self.cleaned_data["middle_name"]
        return data

    def clean_last_name(self):
        data = self.cleaned_data["last_name"]
        return data

    def clean(self):
        cleaned_data = super(UserProfileUpdateForm, self).clean()
        return cleaned_data

    class Meta:
        model = Users
        fields = (
            'email',
            #'name',
            "first_name",
            "middle_name",
            "last_name",
            'phone_number',
        )


class UserChangePasswordForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email Id",
        min_length=5,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(5), MaxLengthValidator(100), EmailValidator],
        disabled=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "style": "font-weight:bold",
                "placeholder": "",
            }
        ),
    )
    password = forms.CharField(
        label="Current Password",
        min_length=8,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(8), MaxLengthValidator(100)],
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "style": "font-weight:bold",
                "placeholder": "",
            }
        ),
    )
    new_password = forms.CharField(
        label="New Password",
        min_length=8,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(8), MaxLengthValidator(100)],
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "style": "font-weight:bold",
                "placeholder": "",
            }
        ),
    )
    repeat_password = forms.CharField(
        label="Repeat password",
        min_length=8,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(8), MaxLengthValidator(100)],
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "style": "font-weight:bold",
                "placeholder": "",
            }
        ),
    )

    def clean_email(self):
        data = self.cleaned_data["email"]
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address")
        return data

    def clean_password(self):
        password = self.cleaned_data["password"]
        # check for min length
        min_length = 8
        if len(password) < min_length:
            msg = "Password must be at least %s characters long." % (str(min_length))
            self.add_error("password", msg)
        # check for digit
        if sum(c.isdigit() for c in password) < 1:
            msg = "Password must contain at least 1 number."
            self.add_error("password", msg)
        # check for uppercase letter
        if not any(c.isupper() for c in password):
            msg = "Password must contain at least 1 uppercase letter."
            self.add_error("password", msg)
        # check for lowercase letter
        if not any(c.islower() for c in password):
            msg = "Password must contain at least 1 lowercase letter."
            self.add_error("password", msg)

        email = self.cleaned_data["email"]
        try:
            user = Users.objects.get(user_username=email)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            user = None
        if user is None:
            raise forms.ValidationError("Incorrect current password")
        else:
            if not check_password(password, user.user_password):
                raise forms.ValidationError("Incorrect current password")
            else:
                return password

    def clean_new_password(self):
        new_password = self.cleaned_data["new_password"]
        # check for min length
        min_length = 8
        if len(new_password) < min_length:
            msg = "Password must be at least %s characters long." % (str(min_length))
            self.add_error("new_password", msg)
        # check for digit
        if sum(c.isdigit() for c in new_password) < 1:
            msg = "Password must contain at least 1 number."
            self.add_error("new_password", msg)
        # check for uppercase letter
        if not any(c.isupper() for c in new_password):
            msg = "Password must contain at least 1 uppercase letter."
            self.add_error("new_password", msg)
        # check for lowercase letter
        if not any(c.islower() for c in new_password):
            msg = "Password must contain at least 1 lowercase letter."
            self.add_error("new_password", msg)
        return new_password

    def clean(self):
        cleaned_data = super(UserChangePasswordForm, self).clean()

        new_password = cleaned_data.get("new_password")
        repeat_password = cleaned_data.get("repeat_password")
        if new_password and repeat_password:
            if new_password != repeat_password:
                msg = "Password doesn't match."
                self.add_error("repeat_password", msg)
        return cleaned_data

    class Meta:
        model = Users
        fields = (
            "email",
            "password",
            "new_password",
            "repeat_password",
        )
