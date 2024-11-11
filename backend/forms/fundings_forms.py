from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator

from app.models.organizations import Organizations
from app.models.fundings import Fundings
from app.models.levels import Levels
from django.utils.html import strip_tags
from app.models.users import Users

class FundingsSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(FundingsSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Fundings
        fields = ()


class FundingsCreateForm(forms.ModelForm):
    organization = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Organization",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_organization",
                "class": "form-control data",
                "style": "width:100%;",
                "placeholder": "",
                
            }
        ))
    
    amount = forms.CharField(
        label='Amount',
        min_length=1,
        max_length=1000,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(100)],
        widget=forms.TextInput(
            attrs={
                "id": "amount",
                'class': 'form-control data',
                'placeholder': '',
            }
        ),
    )

    currency = forms.ChoiceField(
        choices= (('', '--select--'),),
        initial="",
        label="Currency",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "currency",
                "class": "form-control data",
                "style": "width:100%;",
                "placeholder": "",
                
            }
        ))
    
    def clean_organization(self):
        data = strip_tags(self.cleaned_data["organization"])
        return data
    
    def clean_amount(self):
        data = strip_tags(self.cleaned_data['amount'])
        return data
    
    def clean_currency(self):
        data = strip_tags(self.cleaned_data['currency'])
        return data

    def clean(self):
        cleaned_data = super(FundingsCreateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(FundingsCreateForm, self).__init__(*args, **kwargs)

        ORGANIZATIONS= (('', '--select--'),)
        organizations = Organizations.objects.all()
        for item in organizations:
            ORGANIZATIONS=ORGANIZATIONS+ \
                ((item.organization_id, item.organization_name),)
            
        self.fields['organization'] = forms.ChoiceField(
        choices= ORGANIZATIONS,
        initial="",
        label="Organization",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_organization",
                "class": "form-control data",
                "style": "width:100%;",
                "placeholder": "",
                
            }
        ))

        CURRENCIES = (("RWF", "RWF"),) 
        currencies = Levels.objects.filter(level_key = 'currency', level_parent = 0).order_by("level_id")
        for item in currencies:
                    CURRENCIES = CURRENCIES + \
                        ((str(item.level_name), str(item.level_name)),)
                    
        self.fields['currency'] = forms.ChoiceField(
        choices= CURRENCIES,
        initial="",
        label="Currency",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "currency",
                "class": "form-control data",
                "style": "width:100%;",
                "placeholder": "",
                
            }
        ))

    class Meta:
        model = Fundings
        fields = (
            'organization',
            'amount',
            'currency',
        )


class FundingsUpdateForm(forms.ModelForm):
    organization = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Organization",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_organization",
                "class": "form-control data",
                "style": "width:100%;",
                "placeholder": "",
                
            }
        ))
    
    amount = forms.CharField(
        label='Amount',
        min_length=1,
        max_length=1000,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(100)],
        widget=forms.TextInput(
            attrs={
                "id": "amount",
                'class': 'form-control data',
                'placeholder': '',
            }
        ),
    )

    currency = forms.ChoiceField(
        choices= (('', '--select--'),),
        initial="",
        label="Currency",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "currency",
                "class": "form-control data",
                "style": "width:100%;",
                "placeholder": "",
                
            }
        ))
    def clean_organization(self):
        data = strip_tags(self.cleaned_data["organization"])
        return data
    
    def clean_amount(self):
        data = strip_tags(self.cleaned_data['amount'])
        return data
    
    def clean_currency(self):
        data = strip_tags(self.cleaned_data['currency'])
        return data

    def clean(self):
        cleaned_data = super(FundingsUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(FundingsUpdateForm, self).__init__(*args, **kwargs)

        ORGANIZATIONS= (('', '--select--'),)
        organizations = Organizations.objects.all()
        for item in organizations:
            ORGANIZATIONS=ORGANIZATIONS+ \
                ((item.organization_id, item.organization_name),)
            
        self.fields['organization'] = forms.ChoiceField(
        choices= ORGANIZATIONS,
        initial="",
        label="Organization",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_organization",
                "class": "form-control data",
                "style": "width:100%;",
                "placeholder": "",
                
            }
        ))

        CURRENCIES = (("RWF", "RWF"),) 
        currencies = Levels.objects.filter(level_key = 'currency', level_parent = 0).order_by("level_id")
        for item in currencies:
                    CURRENCIES = CURRENCIES + \
                        ((str(item.level_name), str(item.level_name)),)
                    
        self.fields['currency'] = forms.ChoiceField(
        choices= CURRENCIES,
        initial="",
        label="Currency",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "currency",
                "class": "form-control data",
                "style": "width:100%;",
                "placeholder": "",
                
            }
        ))

    class Meta:
        model = Fundings
        fields = (
            'organization',
            'amount',
            'currency',
        )
    

class FundingsViewForm(forms.ModelForm):

    organization = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Organization",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_organization",
                "class": "form-control data",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,   
            }
        ))
    
    amount = forms.CharField(
        label='Amount',
        min_length=1,
        max_length=1000,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(100)],
        widget=forms.TextInput(
            attrs={
                "id": "amount",
                'class': 'form-control data',
                'placeholder': '',
                "readonly": True,
            }
        ),
    )

    currency = forms.ChoiceField(
        choices= (('', '--select--'),),
        initial="",
        label="Currency",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "currency",
                "class": "form-control data",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                
            }
        ))
    
    def clean_organization(self):
        data = strip_tags(self.cleaned_data["organization"])
        return data
    
    def clean_amount(self):
        data = strip_tags(self.cleaned_data['amount'])
        return data
    
    def clean_currency(self):
        data = strip_tags(self.cleaned_data['currency'])
        return data

    def clean(self):
        cleaned_data = super(FundingsViewForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(FundingsViewForm, self).__init__(*args, **kwargs)

        ORGANIZATIONS= (('', '--select--'),)
        organizations = Organizations.objects.all()
        for item in organizations:
            ORGANIZATIONS=ORGANIZATIONS+ \
                ((item.organization_id, item.organization_name),)
            
        self.fields['organization'] = forms.ChoiceField(
        choices= ORGANIZATIONS,
        initial="",
        label="Organization",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_organization",
                "class": "form-control data",
                "style": "width:100%;",
                "placeholder": "",
                
            }
        ))

        CURRENCIES = (("RWF", "RWF"),) 
        currencies = Levels.objects.filter(level_key = 'currency', level_parent = 0).order_by("level_id")
        for item in currencies:
                    CURRENCIES = CURRENCIES + \
                        ((str(item.level_name), str(item.level_name)),)
                    
        self.fields['currency'] = forms.ChoiceField(
        choices= CURRENCIES,
        initial="",
        label="Currency",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "currency",
                "class": "form-control data",
                "style": "width:100%;",
                "placeholder": "",
                
            }
        ))

    class Meta:
        model = Fundings
        fields = (
            'organization',
            'amount',
            'currency',
        )