from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator

from app.models.levels import Levels


class LevelsSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(LevelsSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Levels
        fields = ()


class LevelsCreateForm(forms.ModelForm):
    key = forms.ChoiceField(
        choices=(
            ("organization-status", "organization-status"),
            ("organization-type", "organization-type"),
            ("financing-agent-type", "financing-agent-type"),
            ("financing-scheme-type", "financing-scheme-type"),
            ("financing-source-type", "financing-source-type"),
            ("health-provider-type", "health-provider-type"),
            ("capital-formation", "capital-formation"),
            ("function", "function"),
            ("sub-function", "sub-function"),
            ("inputs", "inputs"),
            ("domain", "domain"),
            ("sub-domain","sub-domain"),
            ("location", "location"),
            ("currency", "currency"),
            
        ),
        initial="",
        label="Key",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-key",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    code = forms.CharField(
        label="Code",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    name = forms.CharField(
        label="Name",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    parent = forms.CharField(
        label="Parent",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-parent",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    def clean_key(self):
        data = self.cleaned_data["key"]
        return data

    def clean_code(self):
        data = self.cleaned_data["code"]
        return data

    def clean_name(self):
        data = self.cleaned_data["name"]
        return data
    
    def clean_parent(self):
        data = self.cleaned_data["parent"]
        return data

    def clean(self):
        cleaned_data = super(LevelsCreateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(LevelsCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Levels
        fields = (
            "key",
            "code",
            "name",
            "parent",
        )


class LevelsUpdateForm(forms.ModelForm):
    key = forms.ChoiceField(
        choices=(
            ("organization-status", "organization-status"),
            ("organization-type", "organization-type"),
            ("financing-agent-type", "financing-agent-type"),
            ("financing-scheme-type", "financing-scheme-type"),
            ("health-provider-type", "health-provider-type"),
            ("capital-formation", "capital-formation"),
            ("functions", "functions"),
            ("programs", "programs"),
            ("inputs", "inputs"),
            ("location", "location"),
            ("currency", "currency"),
        ),
        initial="",
        label="Key",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-key",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    code = forms.CharField(
        label="Code",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    name = forms.CharField(
        label="Name",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    parent = forms.CharField(
        label="Parent",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-parent",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    def clean_key(self):
        data = self.cleaned_data["key"]
        return data

    def clean_code(self):
        data = self.cleaned_data["code"]
        return data

    def clean_name(self):
        data = self.cleaned_data["name"]
        return data
    
    def clean_parent(self):
        data = self.cleaned_data["parent"]
        return data

    def clean(self):
        cleaned_data = super(LevelsUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(LevelsUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Levels
        fields = (
            "key",
            "code",
            "name",
            "parent",
        )


class LevelsViewForm(forms.ModelForm):
    key = forms.ChoiceField(
        choices=(
            ("organization-status", "organization-status"),
            ("organization-type", "organization-type"),
            ("financing-agent-type", "financing-agent-type"),
            ("financing-scheme-type", "financing-scheme-type"),
            ("health-provider-type", "health-provider-type"),
            ("capital-formation", "capital-formation"),
            ("functions", "functions"),
            ("programs", "programs"),
            ("inputs", "inputs"),
            ("location", "location"),
            ("currency", "currency"),
        ),
        initial="",
        label="Key",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-key",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    code = forms.CharField(
        label="Code",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    name = forms.CharField(
        label="Name",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    parent = forms.CharField(
        label="Parent",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-parent",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    def clean_key(self):
        data = self.cleaned_data["key"]
        return data

    def clean_code(self):
        data = self.cleaned_data["code"]
        return data

    def clean_name(self):
        data = self.cleaned_data["name"]
        return data
    
    def clean_parent(self):
        data = self.cleaned_data["parent"]
        return data

    def clean(self):
        cleaned_data = super(LevelsViewForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(LevelsViewForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Levels
        fields = (
            "key",
            "code",
            "name",
            "parent",
        )
