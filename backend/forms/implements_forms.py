from app.models.implementers import Implementers
from app.models.users import Users
from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from tinymce.widgets import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class ImplementersSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(ImplementersSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Implementers
        fields = ()


class ImplementersCreateForm(forms.ModelForm):
    name = forms.CharField(
        label="Add Implementer",
        min_length=1,
        max_length=1000,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(1000)],
        widget=forms.TextInput(
            attrs={
                "id": "id_name_implementers",
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )

    def clean_name(self):
        data = self.cleaned_data["name"]
        return data

    def clean(self):
        cleaned_data = super(ImplementersCreateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(ImplementersCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Implementers
        fields = ("name",)


class ImplementersUpdateForm(forms.ModelForm):
    name = forms.CharField(
        label="Implementer name",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_name_implementers",
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )

    def clean_name(self):
        data = self.cleaned_data["name"]
        return data

    def clean(self):
        cleaned_data = super(ImplementersUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(ImplementersUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Implementers
        fields = ("name",)


class ImplementersViewForm(forms.ModelForm):
    name = forms.CharField(
        label="Implementer name",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_name_implementers",
                "class": "form-control",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    def clean_name(self):
        data = self.cleaned_data["name"]
        return data

    def clean(self):
        cleaned_data = super(ImplementersViewForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(ImplementersViewForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Implementers
        fields = ("name",)

class ImplementersCreateHtmlForm(forms.ModelForm):
    name = forms.CharField(
        label="Add Implementer",
        required=True,
        widget=TinyMCEWidget(
            attrs={
                "required": False,
                "id": "id_name_implementers",
                "rows": 6,
                "cols": 110,
            }
        ),
    )

    def clean_name(self):
        data = self.cleaned_data["name"]
        return data

    def clean(self):
        cleaned_data = super(ImplementersCreateHtmlForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(ImplementersCreateHtmlForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Implementers
        fields = ("name",)
