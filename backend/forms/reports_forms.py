from django import forms
from datetime import date
from django.core.validators import MaxLengthValidator, MinLengthValidator

from app.models.organizations import Organizations
from app.models.reports import Reports
from app.models.levels import Levels
from app.models.users import Users
from app.utils import Utils

class ReportsSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(ReportsSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Reports
        fields = ()


class ReportsCreateForm(forms.ModelForm):
    asset_name = forms.CharField(
        label="Asset Name",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ))
    
    capital_class = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Capital Class",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_capital_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ))
    
    capital_sub_class = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Capital Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_capital_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ))
    purchase_value= forms.CharField(
        label='Purchase value',
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ))
    purchase_currency =forms.ChoiceField(
        choices= (("0", "--Select--"),),
        label="Purchase Value Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    book_value = forms.CharField(
        label='Book Value',
        min_length=1,
        max_length=1000,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(100)],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '',
            }
        ),
    )
    book_currency =forms.ChoiceField(
        choices= (("0", "--Select--"),),
        label="Book value Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    year_purchased = forms.ChoiceField(
        choices= Utils.get_year_choices(),
        initial= date.today().year,
        label='Year Purchased',
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': '',
            }
        ),
    )
    
    funding_source = forms.MultipleChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Funding Source",
        required=False,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_report_funding_source",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    
    fiscal_year =forms.ChoiceField(
        choices=Utils.get_fiscal_year_choices(),
        initial="",
        label="Fiscal Year",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_fiscal_year",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
        )

    def clean_asset_name(self):
        data = self.cleaned_data["asset_name"]
        return data
    
    def clean_capital_class(self):
        data = self.cleaned_data["capital_class"]
        return data
    
    def clean_capital_sub_class(self):
        data = self.cleaned_data["capital_sub_class"]
        return data
    
    def clean_purchase_value(self):
        data = self.cleaned_data['purchase_value']
        return data
    
    def clean_purchase_currency(self):
        data = self.cleaned_data["purchase_currency"]
        return data
    
    def clean_book_value(self):
        data = self.cleaned_data['book_value']
        return data
    
    def clean_book_currency(self):
        data = self.cleaned_data["book_currency"]
        return data
    
    def clean_year_purchased(self):
        data = self.cleaned_data['year_purchased']
        return data
    
    def clean_funding_source(self):
        data = self.cleaned_data['funding_source']
        return data
    
    def clean_fiscal_year(self):
        data = self.cleaned_data["fiscal_year"]
        return data
    
    def clean(self):
        cleaned_data = super(ReportsCreateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(ReportsCreateForm, self).__init__(*args, **kwargs)

        CAPITAL = (("0", "--Select--"),)
        capitals_ = Levels.objects.filter(level_key = 'capital-formation', level_parent = 0).order_by("level_id") 
        for item in capitals_:
            CAPITAL = CAPITAL + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 

        self.fields['capital_class'] = forms.ChoiceField(
        choices= CAPITAL,
        initial="",
        label="Capital Class",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_capital_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ))
        
        SUBCAPITAL = (("0", "NONE"),)
        subcapitals_ = Levels.objects.filter(level_key = 'capital-formation').order_by("level_id") 
        for item in subcapitals_:
            SUBCAPITAL = SUBCAPITAL + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 
    
        self.fields['capital_sub_class'] = forms.ChoiceField(
            choices= SUBCAPITAL,
            initial="",
            label="Capital Sub Class",
            required=False,
            validators=[],
            widget=forms.Select(
                attrs={
                    "id": "id_capital_sub_class",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ))
        CURRENCIES = (("RWF", "RWF"),) 
        currencies = Levels.objects.filter(level_key = 'currency', level_parent = 0).order_by("level_id")
        for item in currencies:
                    CURRENCIES = CURRENCIES + \
                        ((str(item.level_name), str(item.level_name)),)
        self.fields['purchase_currency']=forms.ChoiceField(
            choices= CURRENCIES,
            label="Purchase Value Currency",
            required=False,
            widget=forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "",
                }
            ),)
        
        self.fields['book_currency'] =forms.ChoiceField(
            choices= CURRENCIES,
            label="Book value Currency",
            required=False,
            widget=forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "",
                }
            ),)
        
        ORGANIZATIONS = (('', '--select--'),)
        organizations = Organizations.objects.all()
        for item in organizations:
                        ORGANIZATIONS = ORGANIZATIONS + \
                            ((item.organization_id, item.organization_name),)
                    
        self.fields['funding_source'] = forms.MultipleChoiceField(
            choices= ORGANIZATIONS[1:],
            initial="",
            label="Funding Source",
            required=False,
            validators=[],
            widget=forms.SelectMultiple(
                attrs={
                    "id": "id_report_funding_source",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ),)

    class Meta:
        model = Reports
        fields = (
            "asset_name",
            "capital_class",
            "capital_sub_class",
            "purchase_value",
            "purchase_currency",
            "book_value",
            "book_currency",
            "year_purchased",
            "funding_source",
            "fiscal_year"
        )


class ReportsUpdateForm(forms.ModelForm):

    asset_name = forms.CharField(
        label='Report Title',
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ))
    
    capital_class = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Capital Class",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_capital_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ))
    
    capital_sub_class = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Capital Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_capital_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ))
    purchase_value= forms.CharField(
        label='Purchase value',
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ))
    purchase_currency =forms.ChoiceField(
        choices= (("0", "--Select--"),),
        label="Purchase Value Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    book_value = forms.CharField(
        label='Book Value',
        min_length=1,
        max_length=1000,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(100)],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '',
            }
        ),
    )
    book_currency =forms.ChoiceField(
        choices= (("0", "--Select--"),),
        label="Book value Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    year_purchased = forms.ChoiceField(
        choices= Utils.get_year_choices(),
        label='Year Purchased',
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': '',
            }
        ),
    )
    
    funding_source = forms.MultipleChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Funding Source",
        required=False,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_report_funding_source",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    
    fiscal_year = forms.ChoiceField(
        choices=Utils.get_fiscal_year_choices(),
        initial="",
        label="Fiscal Year",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_fiscal_year",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
        )

    def clean_asset_name(self):
        data = self.cleaned_data["asset_name"]
        return data
    
    def clean_capital_class(self):
        data = self.cleaned_data["capital_class"]
        return data
    
    def clean_capital_sub_class(self):
        data = self.cleaned_data["capital_sub_class"]
        return data
    def clean_purchase_value(self):
        data = self.cleaned_data['purchase_value']
        return data
    
    def clean_purchase_currency(self):
        data = self.cleaned_data["purchase_currency"]
        return data
    
    def clean_book_value(self):
        data = self.cleaned_data['book_value']
        return data
    
    def clean_book_currency(self):
        data = self.cleaned_data["book_currency"]
        return data
    
    def clean_year_purchased(self):
        data = self.cleaned_data['year_purchased']
        return data
    
    def clean_funding_source(self):
        data = self.cleaned_data['funding_source']
        return data
    
    def clean_funds_transfer_class(self):
        data = self.cleaned_data["funds_transfer_class"]
        return data
    
    def clean_funds_transfer_sub_class(self):
        data = self.cleaned_data["funds_transfer_sub_class"]
        return data
    
    def clean_fiscal_year(self):
        data = self.cleaned_data["fiscal_year"]
        return data
    def clean(self):
        cleaned_data = super(ReportsUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(ReportsUpdateForm, self).__init__(*args, **kwargs)
        CAPITAL = (("0", "--Select--"),)
        capitals_ = Levels.objects.filter(level_key = 'capital-formation', level_parent = 0).order_by("level_id") 
        for item in capitals_:
            CAPITAL = CAPITAL + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 

        self.fields['capital_class'] = forms.ChoiceField(
        choices= CAPITAL,
        initial="",
        label="Capital Class",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_capital_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ))
        
        SUBCAPITAL = (("0", "NONE"),)
        subcapitals_ = Levels.objects.filter(level_key = 'capital-formation').order_by("level_id") 
        for item in subcapitals_:
            SUBCAPITAL = SUBCAPITAL + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 
    
        self.fields['capital_sub_class'] = forms.ChoiceField(
            choices= SUBCAPITAL,
            initial="",
            label="Capital Sub Class",
            required=False,
            validators=[],
            widget=forms.Select(
                attrs={
                    "id": "id_capital_sub_class",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ))
        CURRENCIES = (("RWF", "RWF"),) 
        currencies = Levels.objects.filter(level_key = 'currency', level_parent = 0).order_by("level_id")
        for item in currencies:
                    CURRENCIES = CURRENCIES + \
                        ((str(item.level_name), str(item.level_name)),)
        self.fields['purchase_currency']=forms.ChoiceField(
            choices= CURRENCIES,
            label="Purchase Value Currency",
            required=False,
            widget=forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "",
                }
            ),)
        
        self.fields['book_currency'] =forms.ChoiceField(
            choices= CURRENCIES,
            label="Book value Currency",
            required=False,
            widget=forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "",
                }
            ),)
        
        ORGANIZATIONS = (('', '--select--'),)
        organizations = Organizations.objects.all()
        for item in organizations:
                        ORGANIZATIONS = ORGANIZATIONS + \
                            ((item.organization_id, item.organization_name),)
                    
        self.fields['funding_source'] = forms.MultipleChoiceField(
            choices= ORGANIZATIONS[1:],
            initial="",
            label="Funding Source",
            required=False,
            validators=[],
            widget=forms.SelectMultiple(
                attrs={
                    "id": "id_report_funding_source",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ),)


    class Meta:
        model = Reports
        fields = (
             "asset_name",
            "capital_class",
            "capital_sub_class",
            "purchase_value",
            "purchase_currency",
            "book_value",
            "book_currency",
            "year_purchased",
            "funding_source",
            "fiscal_year"
        )


class ReportsViewForm(forms.ModelForm):

    asset_name = forms.CharField(
        label='Report Title',
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ))
    
    capital_class = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Capital Class",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_capital_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ))
    
    capital_sub_class = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Capital Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_capital_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ))
    purchase_value= forms.CharField(
        label='Purchase value',
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ))
    purchase_currency =forms.ChoiceField(
        choices= (("0", "--Select--"),),
        label="Purchase Value Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    book_value = forms.CharField(
        label='Book Value',
        min_length=1,
        max_length=1000,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(100)],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '',
            }
        ),
    )
    book_currency =forms.ChoiceField(
        choices= (("0", "--Select--"),),
        label="Book value Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )
    
    year_purchased = forms.ChoiceField(
        choices= Utils.get_year_choices(),
        initial= date.today().year,
        label='Year Purchased',
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': '',
            }
        ),
    )
    
    funding_source =forms.MultipleChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Funding Source",
        required=False,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_report_funding_source",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    
    fiscal_year = forms.ChoiceField(
        choices=Utils.get_fiscal_year_choices(),
        initial="",
        label="Fiscal Year",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_fiscal_year",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
        )

    def clean_asset_name(self):
        data = self.cleaned_data["asset_name"]
        return data
    
    def clean_capital_class(self):
        data = self.cleaned_data["capital_class"]
        return data
    
    def clean_capital_sub_class(self):
        data = self.cleaned_data["capital_sub_class"]
        return data
    
    def clean_purchase_value(self):
        data = self.cleaned_data['purchase_value']
        return data
    
    def clean_purchase_currency(self):
        data = self.cleaned_data["purchase_currency"]
        return data
    
    def clean_book_value(self):
        data = self.cleaned_data['book_value']
        return data
    
    def clean_book_currency(self):
        data = self.cleaned_data["book_currency"]
        return data
    
    def clean_year_purchased(self):
        data = self.cleaned_data['year_purchased']
        return data
    
    def clean_funding_source(self):
        data = self.cleaned_data['funding_source']
        return data
    
    def clean_funds_transfer_class(self):
        data = self.cleaned_data["funds_transfer_class"]
        return data
    
    def clean_funds_transfer_sub_class(self):
        data = self.cleaned_data["funds_transfer_sub_class"]
        return data
    
    def clean_fiscal_year(self):
        data = self.cleaned_data["fiscal_year"]
        return data

    def clean(self):
        cleaned_data = super(ReportsViewForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(ReportsViewForm, self).__init__(*args, **kwargs)
        CAPITAL = (("0", "--Select--"),)
        capitals_ = Levels.objects.filter(level_key = 'capital-formation', level_parent = 0).order_by("level_id") 
        for item in capitals_:
            CAPITAL = CAPITAL + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 

        self.fields['capital_class'] = forms.ChoiceField(
        choices= CAPITAL,
        initial="",
        label="Capital Class",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_capital_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ))
        
        SUBCAPITAL = (("0", "NONE"),)
        subcapitals_ = Levels.objects.filter(level_key = 'capital-formation').order_by("level_id") 
        for item in subcapitals_:
            SUBCAPITAL = SUBCAPITAL + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 
    
        self.fields['capital_sub_class'] = forms.ChoiceField(
            choices= SUBCAPITAL,
            initial="",
            label="Capital Sub Class",
            required=False,
            validators=[],
            widget=forms.Select(
                attrs={
                    "id": "id_capital_sub_class",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ))
        CURRENCIES = (("RWF", "RWF"),) 
        currencies = Levels.objects.filter(level_key = 'currency', level_parent = 0).order_by("level_id")
        for item in currencies:
                    CURRENCIES = CURRENCIES + \
                        ((str(item.level_name), str(item.level_name)),)
        self.fields['purchase_currency']=forms.ChoiceField(
            choices= CURRENCIES,
            label="Purchase Value Currency",
            required=False,
            widget=forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "",
                }
            ),)
        
        self.fields['book_currency'] =forms.ChoiceField(
            choices= CURRENCIES,
            label="Book value Currency",
            required=False,
            widget=forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "",
                }
            ),)
        
        ORGANIZATIONS = (('', '--select--'),)
        organizations = Organizations.objects.all()
        for item in organizations:
                        ORGANIZATIONS = ORGANIZATIONS + \
                            ((item.organization_id, item.organization_name),)
                    
        self.fields['funding_source'] = forms.MultipleChoiceField(
            choices= ORGANIZATIONS[1:],
            initial="",
            label="Funding Source",
            required=False,
            validators=[],
            widget=forms.SelectMultiple(
                attrs={
                    "id": "id_report_funding_source",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ),)


    class Meta:
        model = Reports
        fields = (
            "asset_name",
            "capital_class",
            "capital_sub_class",
            "purchase_value",
            "purchase_currency",
            "book_value",
            "book_currency",
            "year_purchased",
            "funding_source",
            "fiscal_year"
        )
