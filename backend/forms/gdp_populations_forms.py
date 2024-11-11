import re
from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from app.models.gdp_populations import Gdp_Populations
from app.utils import Utils

class GdpPopulationsSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(GdpPopulationsSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Gdp_Populations
        fields = ()


class GdpPopulationsCreateForm(forms.ModelForm):
    fiscal_year= forms.ChoiceField(
        choices= Utils.get_fiscal_year_choices(),
        initial="",
        label="Fiscal Year",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_fiscal-year",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    population = forms.CharField(
        label="Total Population",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_population",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    
    budget = forms.CharField(
        label="Total Government bugdet",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_budget",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    expenditure = forms.CharField(
        label="Total Government Expenditure",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_expenditure",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    gdp = forms.CharField(
        label="Current GDP(in billions RWF)",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_gdp",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    payment_rate = forms.CharField(
        label="OOP-Public HF(Co-payment) Rate of IGR in Public Facilities in %",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_payment_rate",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    
    budget_health = forms.CharField(
        label="Government Bugdet on Health",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_budget_health",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    expenditure_health = forms.CharField(
        label="Government Expenditure on Health",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_expenditure_health",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )


    def clean_fiscal_year(self):
        data = self.cleaned_data["fiscal_year"]
        return data

    def clean_population(self):
        data = self.cleaned_data["population"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid decimal format")
        
    def clean_budget(self):
        data = self.cleaned_data["budget"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid number")
        
    def clean_expenditure(self):
        data = self.cleaned_data["expenditure"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid Number")
    
    
    def clean_gdp(self):
        data = self.cleaned_data["gdp"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid decimal format")

    def clean_payment_rate(self):
        data = self.cleaned_data["payment_rate"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid decimal format")
    
    def clean_budget_health(self):
        data = self.cleaned_data["budget_health"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid number")
        
    def clean_expenditure_health(self):
        data = self.cleaned_data["expenditure_health"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid Number")

    def clean(self):
        cleaned_data = super(GdpPopulationsCreateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(GdpPopulationsCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Gdp_Populations
        fields = (
            "fiscal_year",
            "population",
            "budget",
            "expenditure",
            "gdp",
            "payment_rate",
            "budget_health",
            "expenditure_health",
        )


class GdpPopulationsUpdateForm(forms.ModelForm):
    fiscal_year= forms.ChoiceField(
        choices=Utils.get_fiscal_year_choices(),
        label="Fiscal Year",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_fiscal-year",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
            }
        ),
    )
    population = forms.CharField(
        label="Total Population",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_population",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    
    budget = forms.CharField(
        label="Total Government bugdet",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_budget",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    expenditure = forms.CharField(
        label="Total Government Expenditure",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_expenditure",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    budget_health = forms.CharField(
        label="Government Bugdet on Health",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_budget_health",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    expenditure_health = forms.CharField(
        label="Government Expenditure on Health",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_expenditure_health",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    gdp = forms.CharField(
        label="Current GDP(in billions RWF)",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_gdp",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    payment_rate = forms.CharField(
        label="OOP-Public HF(Co-payment) rate of IGR in Public Facilities in %",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_payment_rate",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    def clean_fiscal_year(self):
        data = self.cleaned_data["fiscal_year"]
        return data

    def clean_population(self):
        data = self.cleaned_data["population"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid decimal format")

    def clean_budget(self):
        data = self.cleaned_data["budget"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid number")
        
    def clean_expenditure(self):
        data = self.cleaned_data["expenditure"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid Number")
        
    def clean_gdp(self):
        data = self.cleaned_data["gdp"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid decimal format")

    def clean_payment_rate(self):
        data = self.cleaned_data["payment_rate"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid decimal format")
        
    def clean_budget_health(self):
        data = self.cleaned_data["budget_health"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid number")
        
    def clean_expenditure_health(self):
        data = self.cleaned_data["expenditure_health"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid Number")

    def clean(self):
        cleaned_data = super(GdpPopulationsUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(GdpPopulationsUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Gdp_Populations
        fields = (
            "fiscal_year",
            "population",
            "budget",
            "expenditure",
            "gdp",
            "payment_rate",
            "budget_health",
            "expenditure_health",
        )


class GdpPopulationsViewForm(forms.ModelForm):
    fiscal_year= forms.ChoiceField(
        choices=Utils.get_fiscal_year_choices(),
        initial="",
        label="Fiscal Year",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_fiscal-year",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
            }
        ),
    )
    population = forms.CharField(
        label="Total Population",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_population",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
            }
        ),
    )
    
    budget = forms.CharField(
        label="Total Government bugdet",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_budget",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    expenditure = forms.CharField(
        label="Total Government Expenditure",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_population",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    gdp = forms.CharField(
        label="Current GDP(in billions RWF)",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_gdp",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
            }
        ),
    )
    payment_rate = forms.CharField(
        label="OOP-Public HF(Co-payment) rate of IGR in Public Facilities in %",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_payment_rate",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
            }
        ),
    )
    
    budget_health = forms.CharField(
        label="Government Bugdet on Health",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_budget_health",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    expenditure_health = forms.CharField(
        label="Government Expenditure on Health",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "id": "id_expenditure_health",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    def clean_fiscal_year(self):
        data = self.cleaned_data["fiscal_year"]
        return data

    def clean_population(self):
        data = self.cleaned_data["population"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid decimal format")
        
    def clean_budget(self):
        data = self.cleaned_data["budget"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid number")
        
    def clean_expenditure(self):
        data = self.cleaned_data["expenditure"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid Number")
    
    def clean_gdp(self):
        data = self.cleaned_data["gdp"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid decimal format")

    def clean_payment_rate(self):
        data = self.cleaned_data["payment_rate"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid decimal format")
        
    def clean_budget_health(self):
        data = self.cleaned_data["budget_health"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid number")
        
    def clean_expenditure_health(self):
        data = self.cleaned_data["expenditure_health"]
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid Number")

    def clean(self):
        cleaned_data = super(GdpPopulationsViewForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(GdpPopulationsViewForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Gdp_Populations
        fields = (
            "fiscal_year",
            "population",
            "budget",
            "expenditure",
            "gdp",
            "payment_rate",
            "budget_health",
            "expenditure_health",
        )
