import re
from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from app.models.gdp_populations import Gdp_Populations
from app.utils import Utils
from app.models.currency_rates import Currency_Rates
from app.models.levels import Levels

class CurrencyRatesSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(CurrencyRatesSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Currency_Rates
        fields = ()


class CurrencyRatesCreateForm(forms.ModelForm):
    fiscal_year= forms.ChoiceField(
        choices= Utils.get_fiscal_year_choices(),
        initial="",
        label="Fiscal Year",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "rate-fiscal-year",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    currency = forms.ChoiceField(
        choices= (('', '--select--'),),
        initial="",
        label="Currency to rwf",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "rate-currency",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    rate = forms.CharField(
        label="Rate",
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

    def clean_fiscal_year(self):
        data = self.cleaned_data["fiscal_year"]
        return data

    def clean_currency(self):
        data = self.cleaned_data["currency"]
        return data

    def clean_rate(self):
        data = self.cleaned_data['rate']
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid decimal format")

    def clean(self):
        cleaned_data = super(CurrencyRatesCreateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(CurrencyRatesCreateForm, self).__init__(*args, **kwargs)
        
        CURRENCIES = (("0", "--Select--"),) 
        currencies = Levels.objects.filter(level_key = 'currency', level_parent = 0).order_by("level_id")
        for item in currencies:
                    CURRENCIES = CURRENCIES + \
                        ((str(item.level_name), str(item.level_name)),)
                    
        self.fields['currency'] = forms.ChoiceField(
        choices= CURRENCIES,
        initial="",
        label="Currency to rwf",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "rate-currency",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    class Meta:
        model = Currency_Rates
        fields = (
            "fiscal_year",
            "currency",
            "rate",
        )


class CurrencyRatesUpdateForm(forms.ModelForm):
    fiscal_year= forms.ChoiceField(
        choices=Utils.get_fiscal_year_choices(),
       # choices=Gdp_Populations.FISCAL_YEARS,
        initial="",
        label="Fiscal Year",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-fiscal_year",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    currency = forms.ChoiceField(
        choices= (('', '--select--'),),
        initial="",
        label="Currency to rwf",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "rate-currency",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    rate = forms.CharField(
        label="Rate",
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

    def clean_fiscal_year(self):
        data = self.cleaned_data["fiscal_year"]
        return data

    def clean_currency(self):
        data = self.cleaned_data["currency"]
        return data

    def clean_rate(self):
        data = self.cleaned_data['rate']
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid decimal format")

    def clean(self):
        cleaned_data = super(CurrencyRatesUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(CurrencyRatesUpdateForm, self).__init__(*args, **kwargs)

        CURRENCIES = (("0", "--Select--"),) 
        currencies = Levels.objects.filter(level_key = 'currency', level_parent = 0).order_by("level_id")
        for item in currencies:
                    CURRENCIES = CURRENCIES + \
                        ((str(item.level_name), str(item.level_name)),)
                    
        self.fields['currency'] = forms.ChoiceField(
        choices= CURRENCIES,
        initial="",
        label="Currency to rwf",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "rate-currency",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    class Meta:
        model = Currency_Rates
        fields = (
            "fiscal_year",
            "currency",
            "rate",
        )


class CurrencyRatesViewForm(forms.ModelForm):
    fiscal_year= forms.ChoiceField(
        choices= Utils.get_fiscal_year_choices(),
        #choices=Gdp_Populations.FISCAL_YEARS,
        initial="",
        label="Fiscal Year",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-fiscal_year",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    currency = forms.ChoiceField(
        choices= (('', '--select--'),),
        initial="",
        label="Currency to rwf",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "rate-currency",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    rate = forms.CharField(
        label="Rate",
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

    def clean_fiscal_year(self):
        data = self.cleaned_data["fiscal_year"]
        return data

    def clean_currency(self):
        data = self.cleaned_data["currency"]
        return data

    def clean_rate(self):
        data = self.cleaned_data['rate']
        if isinstance(data, str):
            # Replace comma with a dot
            data = re.sub(r'[, ]', '', data)
        try:
            return float(data)
        except ValueError:
            raise ValidationError("Invalid decimal format")

    def clean(self):
        cleaned_data = super(CurrencyRatesViewForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(CurrencyRatesViewForm, self).__init__(*args, **kwargs)

        CURRENCIES = (("0", "--Select--"),) 
        currencies = Levels.objects.filter(level_key = 'currency', level_parent = 0).order_by("level_id")
        for item in currencies:
                    CURRENCIES = CURRENCIES + \
                        ((str(item.level_name), str(item.level_name)),)
                    
        self.fields['currency'] = forms.ChoiceField(
        choices= CURRENCIES,
        initial="",
        label="Currency to rwf",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "rate-currency",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    class Meta:
        model = Currency_Rates
        fields = (
            "fiscal_year",
            "currency",
            "rate",
        )
