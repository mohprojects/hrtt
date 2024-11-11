# from django import forms
# from app.models.mailing_server_configurations import MailServerConfig

# class MailServerConfigForm(forms.ModelForm):
#     class Meta:
#         model = MailServerConfig
#         fields = '__all__'


from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from app.utils import Utils
from app.models.mailing_server_configurations import MailServerConfig
#from app.models.port_hosts import MailServerConfig
#from app.data import CURRENCIES

class MailServerConfigSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(MailServerConfigSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = MailServerConfig
        fields = ()


class MailServerConfigCreateForm(forms.ModelForm):
    host= forms.CharField(
        label="Host",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_host",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    port = forms.CharField(
        label="Port",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_port",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    username = forms.CharField(
        label="Username",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_username",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.PasswordInput(
            render_value=True,
            attrs={
                "id": "id_password",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    sender= forms.CharField(
        label="Email Sender",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_sender",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    subject = forms.CharField(
        label=" Email Subject",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_subject",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    tls = forms.BooleanField(
        required=False,
        initial=False,
        label="TLS",
        widget=forms.CheckboxInput(
            attrs={
                "id": "id_tls",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    
    ssl = forms.BooleanField(
        required=False,
        initial=False,
        label="SSL",
        widget=forms.CheckboxInput(
            attrs={
                 "id": "id_ssl",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    def clean_host(self):
        data = self.cleaned_data["host"]
        return data

    def clean_port(self):
        data = self.cleaned_data["port"]
        return data
    
    def clean_username(self):
        data = self.cleaned_data["username"]
        return data

    def clean_password(self):
        data = self.cleaned_data["password"]
        return data
    
    def clean_sender(self):
        data = self.cleaned_data["sender"]
        return data

    def clean_subject(self):
        data = self.cleaned_data["subject"]
        return data
    
    def clean_tls(self):
        data = self.cleaned_data["tls"]
        return data

    def clean_ssl(self):
        data = self.cleaned_data["ssl"]
        return data

    def clean(self):
        cleaned_data = super(MailServerConfigCreateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(MailServerConfigCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = MailServerConfig
        fields = (
            "host",
            "port",
            "username",
            "password",
            "sender",
            "subject",
            "tls",
            "ssl"

        )


class MailServerConfigUpdateForm(forms.ModelForm):
    host = forms.CharField(
        label="Host",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_host",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    port = forms.CharField(
        label="Port",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_port",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    username = forms.CharField(
        label="Username",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_username",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.PasswordInput(
            render_value=True,
            attrs={
                "id": "id_password",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    sender= forms.CharField(
        label="Email Sender",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_sender",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    subject = forms.CharField(
        label=" Email Subject",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_subject",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    tls = forms.BooleanField(
        required=False,
        initial=False,
        label="TLS",
        widget=forms.CheckboxInput(
            attrs={
                "id": "id_tls",
            }
        ),
    )
    
    ssl = forms.BooleanField(
        required=False,
        initial=False,
        label="SSL",
        widget=forms.CheckboxInput(
            attrs={
                 "id": "id_ssl",
            }
        ),
    )


    def clean_host(self):
        data = self.cleaned_data["host"]
        return data

    def clean_port(self):
        data = self.cleaned_data["port"]
        return data
    
    def clean_username(self):
        data = self.cleaned_data["username"]
        return data

    def clean_password(self):
        data = self.cleaned_data["password"]
        return data
    
    def clean_sender(self):
        data = self.cleaned_data["sender"]
        return data

    def clean_subject(self):
        data = self.cleaned_data["subject"]
        return data
    
    def clean_tls(self):
        data = self.cleaned_data["tls"]
        return data

    def clean_ssl(self):
        data = self.cleaned_data["ssl"]
        return data

    def clean(self):
        cleaned_data = super(MailServerConfigUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(MailServerConfigUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = MailServerConfig
        fields = (
            "host",
            "port",
            "username",
            "password",
            "sender",
            "subject",
            "tls",
            "ssl"
        )


class MailServerConfigViewForm(forms.ModelForm):
    host = forms.CharField(
        label="Host",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_host",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    port = forms.CharField(
        label="Port",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_port",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    username = forms.CharField(
        label="Username",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_username",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    
    password = forms.CharField(
        label="Password",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.PasswordInput(
            attrs={
                "id": "id_password",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    sender= forms.CharField(
        label="Email Sender",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_sender",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    subject = forms.CharField(
        label=" Email Subject",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_subject",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    tls = forms.CharField(
        label="TLS",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_tls",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    ssl = forms.CharField(
        label="SSL",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.PasswordInput(
            attrs={
                "id": "id_ssl",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    def clean_fiscal_year(self):
        data = self.cleaned_data["fiscal_year"]
        return data

    def clean_host(self):
        data = self.cleaned_data["host"]
        return data

    def clean_port(self):
        data = self.cleaned_data["port"]
        return data
    
    def clean_username(self):
        data = self.cleaned_data["username"]
        return data

    def clean_password(self):
        data = self.cleaned_data["password"]
        return data
    
    def clean_sender(self):
        data = self.cleaned_data["sender"]
        return data

    def clean_subject(self):
        data = self.cleaned_data["subject"]
        return data
    
    def clean_tls(self):
        data = self.cleaned_data["tls"]
        return data

    def clean_ssl(self):
        data = self.cleaned_data["ssl"]
        return data

    def clean(self):
        cleaned_data = super(MailServerConfigViewForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(MailServerConfigViewForm, self).__init__(*args, **kwargs)

    class Meta:
        model = MailServerConfig
        fields = (
            "host",
            "port",
            "username",
            "password",
            "sender",
            "subject",
            "tls",
            "ssl"
        )
