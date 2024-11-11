from django import forms

from app.models.organizations import Organizations
from app.models.levels import Levels
from app.utils import Utils
from django.core.validators import (
    EmailValidator,
    MaxLengthValidator,
    MinLengthValidator,
    validate_email,
    validate_integer
)
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from app.validators import (IsPhoneNumberValidator,IsNameValidator)


class OrganizationsSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(OrganizationsSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Organizations
        fields = ()


class OrganizationsCreateForm(forms.ModelForm):
    name = forms.CharField(
        label="Name",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), 
                    MaxLengthValidator(191),
                    IsNameValidator],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )

    email = forms.EmailField(
        label="Official Email",
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

    phone_number = forms.CharField(
        label="Telephone",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(9), 
                    MaxLengthValidator(15),
                    IsPhoneNumberValidator],
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    type = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Organization Type",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id":"id_orginization_type",
            }
        ),
    )
    sub_type = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Organization Sub Type",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "orginization_sub_type",
            }
        ),
    )

    category = forms.MultipleChoiceField(
        label='Organization Category',
        required=False,
        choices= Organizations.DROPDOWN_STATUS_,
        widget=forms.CheckboxSelectMultiple
        )

    financial_agent_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Financing Agency Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-financial-status-classification",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    financial_agent_sub_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Financing Agency Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-status-class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    financial_schemes_name = forms.CharField(
        label="Financing Schemes Name",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )

    financial_schemes_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Financing Schemes Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "financial_schemes_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    financial_schemes_sub_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Financing Schemes Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "financial_schemes_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    healthcare_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Healthcare Provider Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "healthcare_sources_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    healthcare_sub_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="healthcare Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "healthcare_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    funding_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Funding Source Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "funding_sources_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    funding_sub_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Funding Source Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "funding_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    def clean_name(self):
        data = strip_tags(self.cleaned_data["name"])
        try:
            item = Organizations.objects.get(organization_name=data)
        except (TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            item = None
        if item is not None:
            raise forms.ValidationError('Name: "%s" is already in use.' % data)
        return data

    def clean_email(self):
        data = strip_tags(self.cleaned_data["email"])
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address")
        return data

    def clean_phone_number(self):
        data = strip_tags(self.cleaned_data["phone_number"])
        return data

    def clean_type(self):
        data = strip_tags(self.cleaned_data["type"])
        return data
    
    def clean_sub_type(self):
        data = strip_tags(self.cleaned_data["sub_type"])
        return data

    def clean_category(self):
        data = strip_tags(self.cleaned_data["category"])
        return data

    def clean_financial_agent_class(self):
        data = strip_tags(self.cleaned_data["financial_agent_class"])
        return data

    def clean_financial_agent_sub_class(self):
        data = strip_tags(self.cleaned_data["financial_agent_sub_class"])
        return data
    
    def clean_financial_schemes_name(self):
        data = strip_tags(self.cleaned_data["financial_schemes_name"])
        return data

    def clean_financial_schemes_class(self):
        data = strip_tags(self.cleaned_data["financial_schemes_class"])
        return data

    def clean_financial_schemes_sub_class(self):
        data = strip_tags(self.cleaned_data["financial_schemes_sub_class"])
        return data

    def clean_healthcare_class(self):
        data = strip_tags(self.cleaned_data["healthcare_class"])
        return data

    def clean_healthcare_sub_class(self):
        data = strip_tags(self.cleaned_data["healthcare_sub_class"])
        return data

    def clean_deadline(self):
        data = strip_tags(self.cleaned_data["deadline"])
        if data is None:
            return None
        return str(data)

    def clean(self):
        cleaned_data = super(OrganizationsCreateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(OrganizationsCreateForm, self).__init__(*args, **kwargs)

        ORGANIZATIONTYPES = (("0", "--Select--"),)
        organization_types = Levels.objects.filter(level_key = 'organization-type', level_parent = 0).order_by("level_id")
        for item in organization_types:
                    ORGANIZATIONTYPES = ORGANIZATIONTYPES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
        ORGANIZATIONS= (('', '--select--'),)
        organizations = Organizations.objects.all()
        for item in organizations:
            ORGANIZATIONS=ORGANIZATIONS+ \
                ((item.organization_id, item.organization_name),)
            
        self.fields['type'] = forms.ChoiceField(
        choices=ORGANIZATIONTYPES,
        initial="",
        label="Organization Type",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id":"id_orginization_type",
            }
        ),)

        ORGANIZATIONSUBTYPES = (("0", "NONE"),)
        organization_sub_types = Levels.objects.filter(level_key = 'organization-type').order_by("level_id")
        for item in organization_sub_types:
                    ORGANIZATIONSUBTYPES = ORGANIZATIONSUBTYPES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 

        self.fields['sub_type'] = forms.ChoiceField(
        choices=ORGANIZATIONSUBTYPES,
        initial="",
        label="Organization Sub Type",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "orginization_sub_type",
            }
        ),)

        AGENTSCLASSES = (("0", "--Select--"),)
        agents_classes = Levels.objects.filter(level_key = 'financing-agent-type', level_parent = 0).order_by("level_id") 
        for item in agents_classes:
                    AGENTSCLASSES= AGENTSCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['financial_agent_class'] = forms.ChoiceField(
        choices=AGENTSCLASSES,
        initial="",
        label="Financing Agency Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-financial-status-classification",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        AGENTSSUBCLASSES = (("0", "NONE"),)
        agents_sub_classes = Levels.objects.filter(level_key = 'financing-agent-type').order_by("level_id") 
        for item in agents_sub_classes:
                    AGENTSSUBCLASSES= AGENTSSUBCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
        self.fields['financial_agent_sub_class'] = forms.ChoiceField(
        choices=AGENTSSUBCLASSES,
        initial="",
        label="Financing Agency Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-status-class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        SCHEMESCLASSES = (("0", "--Select--"),)
        schemes_classes = Levels.objects.filter(level_key = 'financing-scheme-type', level_parent = 0).order_by("level_id")
        for item in schemes_classes: 
                    SCHEMESCLASSES = SCHEMESCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 
                    
        self.fields['financial_schemes_class'] = forms.ChoiceField(
        choices=SCHEMESCLASSES,
        initial="",
        label="Financing Schemes Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "financial_schemes_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        SCHEMESSUBCLASSES = (("0", "NONE"),)
        schemes_sub_classes = Levels.objects.filter(level_key = 'financing-scheme-type').order_by("level_id")
        for item in schemes_sub_classes: 
                    SCHEMESSUBCLASSES = SCHEMESSUBCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['financial_schemes_sub_class'] = forms.ChoiceField(
        choices=SCHEMESSUBCLASSES,
        initial="",
        label="Financing Schemes Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "financial_schemes_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        HEALTHCARESCLASSES = (("0", "--Select--"),)
        healthcare_classes = Levels.objects.filter(level_key = 'health-provider-type', level_parent = 0).order_by("level_id")
        for item in healthcare_classes:
                    HEALTHCARESCLASSES= HEALTHCARESCLASSES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
        self.fields['healthcare_class'] = forms.ChoiceField(
        choices=HEALTHCARESCLASSES,
        initial="",
        label="Healthcare Provider Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "healthcare_sources_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        HEALTHCARESSUBCLASSES = (("0", "NONE"),)
        healthcare_sub_classes = Levels.objects.filter(level_key = 'health-provider-type').order_by("level_id")
        for item in healthcare_sub_classes:
                    HEALTHCARESSUBCLASSES= HEALTHCARESSUBCLASSES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['healthcare_sub_class'] = forms.ChoiceField(
        choices=HEALTHCARESSUBCLASSES,
        initial="",
        label="healthcare Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "healthcare_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        FUNDINGS= (("0", "--Select--"),) 
        fundings = Levels.objects.filter(level_key = 'fundings', level_parent = 0).order_by("level_id")
        for item in fundings:
                    FUNDINGS = FUNDINGS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['funding_class'] = forms.ChoiceField(
        choices=FUNDINGS,
        initial="",
        label="Funding Source Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "funding_sources_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        SUBFUNDINGS= (("0", "NONE"),) 
        sub_fundings = Levels.objects.filter(level_key = 'fundings').order_by("level_id")
        for item in sub_fundings:
                    SUBFUNDINGS = SUBFUNDINGS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['funding_sub_class'] = forms.ChoiceField(
        choices=SUBFUNDINGS,
        initial="",
        label="Funding Source Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "funding_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)
        
    class Meta:
        model = Organizations
        fields = (
            "name",
            "email",
            "type",
            "sub_type",
            "phone_number",
            "category",
            "financial_agent_class",
            "financial_agent_sub_class",
            "financial_schemes_name",
            "financial_schemes_class",
            "financial_schemes_sub_class",
            "healthcare_class",
            "healthcare_sub_class",
        )


class OrganizationsUpdateForm(forms.ModelForm):
    name = forms.CharField(
        label="Name",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), 
                    MaxLengthValidator(191),
                    IsNameValidator],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )

    email = forms.EmailField(
        label="Official Email",
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

    phone_number = forms.CharField(
        label="Telephone",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(9), 
                    MaxLengthValidator(15),
                    IsPhoneNumberValidator],
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    type = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Organization Type",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id":"id_orginization_type",
            }
        ),
    )
    sub_type = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Organization Sub Type",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "orginization_sub_type",
            }
        ),
    )

    category = forms.MultipleChoiceField(
        label='Organization Category',
        required=False,
        choices= Organizations.DROPDOWN_STATUS_,
        widget=forms.CheckboxSelectMultiple
        )

    financial_agent_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Financing Agency Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-financial-status-classification",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    financial_agent_sub_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Financing Agency Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-status-class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    financial_schemes_name = forms.CharField(
        label="Financing Schemes Name",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )

    financial_schemes_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Financing Schemes Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "financial_schemes_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    financial_schemes_sub_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Financing Schemes Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "financial_schemes_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    healthcare_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Healthcare Provider Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "healthcare_sources_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    healthcare_sub_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="healthcare Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "healthcare_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    funding_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Funding Source Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "funding_sources_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    funding_sub_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Funding Source Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "funding_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    def clean_name(self):
        data = strip_tags(self.cleaned_data["name"])
        return data

    def clean_email(self):
        data = strip_tags(self.cleaned_data["email"])
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address")
        return data

    def clean_phone_number(self):
        data = strip_tags(self.cleaned_data["phone_number"])
        return data

    def clean_type(self):
        data = strip_tags(self.cleaned_data["type"])
        return data
    
    def clean_sub_type(self):
        data = strip_tags(self.cleaned_data["sub_type"])
        return data

    def clean_category(self):
        data = strip_tags(self.cleaned_data["category"])
        return data

    def clean_financial_agent_class(self):
        data = strip_tags(self.cleaned_data["financial_agent_class"])
        return data

    def clean_financial_agent_sub_class(self):
        data = strip_tags(self.cleaned_data["financial_agent_sub_class"])
        return data
    
    def clean_financial_schemes_name(self):
        data = strip_tags(self.cleaned_data["financial_schemes_name"])
        return data

    def clean_financial_schemes_class(self):
        data = strip_tags(self.cleaned_data["financial_schemes_class"])
        return data

    def clean_financial_schemes_sub_class(self):
        data = strip_tags(self.cleaned_data["financial_schemes_sub_class"])
        return data

    def clean_healthcare_class(self):
        data = strip_tags(self.cleaned_data["healthcare_class"])
        return data

    def clean_healthcare_sub_class(self):
        data = strip_tags(self.cleaned_data["healthcare_sub_class"])
        return data

    def clean_deadline(self):
        data = strip_tags(self.cleaned_data["deadline"])
        if data is None:
            return None
        return str(data)

    def clean(self):
        cleaned_data = super(OrganizationsUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(OrganizationsUpdateForm, self).__init__(*args, **kwargs)

        ORGANIZATIONTYPES = (("0", "--Select--"),)
        organization_types = Levels.objects.filter(level_key = 'organization-type', level_parent = 0).order_by("level_id")
        for item in organization_types:
                    ORGANIZATIONTYPES = ORGANIZATIONTYPES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)

        ORGANIZATIONS= (('', '--select--'),)
        organizations = Organizations.objects.all()
        for item in organizations:
            ORGANIZATIONS=ORGANIZATIONS+ \
                ((item.organization_id, item.organization_name),)
            
        self.fields['type'] = forms.ChoiceField(
        choices=ORGANIZATIONTYPES,
        initial="",
        label="Organization Type",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id":"id_orginization_type",
            }
        ),)

        ORGANIZATIONSUBTYPES = (("0", "NONE"),)
        organization_sub_types = Levels.objects.filter(level_key = 'organization-type').order_by("level_id")
        for item in organization_sub_types:
                    ORGANIZATIONSUBTYPES = ORGANIZATIONSUBTYPES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 

        self.fields['sub_type'] = forms.ChoiceField(
        choices=ORGANIZATIONSUBTYPES,
        initial="",
        label="Organization Sub Type",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "orginization_sub_type",
            }
        ),)

        AGENTSCLASSES = (("0", "--Select--"),)
        agents_classes = Levels.objects.filter(level_key = 'financing-agent-type', level_parent = 0).order_by("level_id") 
        for item in agents_classes:
                    AGENTSCLASSES= AGENTSCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['financial_agent_class'] = forms.ChoiceField(
        choices=AGENTSCLASSES,
        initial="",
        label="Financing Agency Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-financial-status-classification",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        AGENTSSUBCLASSES = (("0", "NONE"),)
        agents_sub_classes = Levels.objects.filter(level_key = 'financing-agent-type').order_by("level_id") 
        for item in agents_sub_classes:
                    AGENTSSUBCLASSES= AGENTSSUBCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
        self.fields['financial_agent_sub_class'] = forms.ChoiceField(
        choices=AGENTSSUBCLASSES,
        initial="",
        label="Financing Agency Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-status-class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        SCHEMESCLASSES = (("0", "--Select--"),)
        schemes_classes = Levels.objects.filter(level_key = 'financing-scheme-type', level_parent = 0).order_by("level_id")
        for item in schemes_classes: 
                    SCHEMESCLASSES = SCHEMESCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 
                    
        self.fields['financial_schemes_class'] = forms.ChoiceField(
        choices=SCHEMESCLASSES,
        initial="",
        label="Financing Schemes Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "financial_schemes_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        SCHEMESSUBCLASSES = (("0", "NONE"),)
        schemes_sub_classes = Levels.objects.filter(level_key = 'financing-scheme-type').order_by("level_id")
        for item in schemes_sub_classes: 
                    SCHEMESSUBCLASSES = SCHEMESSUBCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['financial_schemes_sub_class'] = forms.ChoiceField(
        choices=SCHEMESSUBCLASSES,
        initial="",
        label="Financing Schemes Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "financial_schemes_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        HEALTHCARESCLASSES = (("0", "--Select--"),)
        healthcare_classes = Levels.objects.filter(level_key = 'health-provider-type', level_parent = 0).order_by("level_id")
        for item in healthcare_classes:
                    HEALTHCARESCLASSES= HEALTHCARESCLASSES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
        self.fields['healthcare_class'] = forms.ChoiceField(
        choices=HEALTHCARESCLASSES,
        initial="",
        label="Healthcare Provider Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "healthcare_sources_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        HEALTHCARESSUBCLASSES = (("0", "NONE"),)
        healthcare_sub_classes = Levels.objects.filter(level_key = 'health-provider-type').order_by("level_id")
        for item in healthcare_sub_classes:
                    HEALTHCARESSUBCLASSES= HEALTHCARESSUBCLASSES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['healthcare_sub_class'] = forms.ChoiceField(
        choices=HEALTHCARESSUBCLASSES,
        initial="",
        label="healthcare Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "healthcare_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        FUNDINGS= (("0", "--Select--"),) 
        fundings = Levels.objects.filter(level_key = 'fundings', level_parent = 0).order_by("level_id")
        for item in fundings:
                    FUNDINGS = FUNDINGS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['funding_class'] = forms.ChoiceField(
        choices=FUNDINGS,
        initial="",
        label="Funding Source Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "funding_sources_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        SUBFUNDINGS= (("0", "NONE"),) 
        sub_fundings = Levels.objects.filter(level_key = 'fundings').order_by("level_id")
        for item in sub_fundings:
                    SUBFUNDINGS = SUBFUNDINGS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['funding_sub_class'] = forms.ChoiceField(
        choices=SUBFUNDINGS,
        initial="",
        label="Funding Source Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "funding_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

         
        
    class Meta:
        model = Organizations
        fields = (
            "name",
            "email",
            "type",
            "sub_type",
            "phone_number",
            "category",
            "financial_agent_class",
            "financial_agent_sub_class",
            "financial_schemes_name",
            "financial_schemes_class",
            "financial_schemes_sub_class",
            "healthcare_class",
            "healthcare_sub_class",
        )


class OrganizationsViewForm(forms.ModelForm):

    name = forms.CharField(
        label="Name",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), 
                    MaxLengthValidator(191),
                    IsNameValidator],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    email = forms.EmailField(
        label="Official Email",
        min_length=5,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(5), MaxLengthValidator(100), EmailValidator],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "style": "font-weight:bold",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    phone_number = forms.CharField(
        label="Telephone",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(9), 
                    MaxLengthValidator(15),
                    IsPhoneNumberValidator],
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
    type = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Organization Type",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id":"id_orginization_type",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    sub_type = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Organization Sub Type",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "orginization_sub_type",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    category = forms.MultipleChoiceField(
        label='Organization Category',
        required=False,
        choices= Organizations.DROPDOWN_STATUS_,
        widget=forms.CheckboxSelectMultiple
        )

    financial_agent_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Financing Agency Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-financial-status-classification",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    financial_agent_sub_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Financing Agency Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-status-class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    financial_schemes_name = forms.CharField(
        label="Financing Schemes Name",
        min_length=1,
        max_length=191,
        required=False,
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

    financial_schemes_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Financing Schemes Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "financial_schemes_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    financial_schemes_sub_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Financing Schemes Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "financial_schemes_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    healthcare_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Healthcare Provider Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "healthcare_sources_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    healthcare_sub_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="healthcare Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "healthcare_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    funding_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Funding Source Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "funding_sources_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    funding_sub_class = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Funding Source Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "funding_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    def clean_name(self):
        data = strip_tags(self.cleaned_data["name"])
        return data
    
    def clean_email(self):
        data = strip_tags(self.cleaned_data["email"])
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address")
        return data

    def clean_phone_number(self):
        data = strip_tags(self.cleaned_data["phone_number"])
        return data

    def clean_type(self):
        data = strip_tags(self.cleaned_data["type"])
        return data
    
    def clean_sub_type(self):
        data = strip_tags(self.cleaned_data["sub_type"])
        return data

    def clean_category(self):
        data = strip_tags(self.cleaned_data["category"])
        return data

    def clean_financial_agent_class(self):
        data = strip_tags(self.cleaned_data["financial_agent_class"])
        return data

    # def clean_financial_agent_class(self):
    #     data = self.cleaned_data["financial_agent_class"]
    #     return data

    def clean_financial_agent_sub_class(self):
        data = strip_tags(self.cleaned_data["financial_agent_sub_class"])
        return data
    
    def clean_financial_schemes_name(self):
        data = strip_tags(self.cleaned_data["financial_schemes_name"])
        return data

    def clean_financial_schemes_class(self):
        data = strip_tags(self.cleaned_data["financial_schemes_class"])
        return data

    def clean_financial_schemes_sub_class(self):
        data = strip_tags(self.cleaned_data["financial_schemes_sub_class"])
        return data

    def clean_healthcare_class(self):
        data = strip_tags(self.cleaned_data["healthcare_class"])
        return data

    def clean_healthcare_sub_class(self):
        data = strip_tags(self.cleaned_data["healthcare_sub_class"])
        return data

    def clean_deadline(self):
        data = strip_tags(self.cleaned_data["deadline"])
        if data is None:
            return None
        return str(data)

  
    def clean(self):
        cleaned_data = super(OrganizationsViewForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(OrganizationsViewForm, self).__init__(*args, **kwargs)
        ORGANIZATIONTYPES = (("0", "--Select--"),)
        organization_types = Levels.objects.filter(level_key = 'organization-type', level_parent = 0).order_by("level_id")
        for item in organization_types:
                    ORGANIZATIONTYPES = ORGANIZATIONTYPES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)

       

        ORGANIZATIONS= (('', '--select--'),)
        organizations = Organizations.objects.all()
        for item in organizations:
            ORGANIZATIONS=ORGANIZATIONS+ \
                ((item.organization_id, item.organization_name),)
            
        self.fields['type'] = forms.ChoiceField(
        choices=ORGANIZATIONTYPES,
        initial="",
        label="Organization Type",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id":"id_orginization_type",
            }
        ),)

        ORGANIZATIONSUBTYPES = (("0", "NONE"),)
        organization_sub_types = Levels.objects.filter(level_key = 'organization-type').order_by("level_id")
        for item in organization_sub_types:
                    ORGANIZATIONSUBTYPES = ORGANIZATIONSUBTYPES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 

        self.fields['sub_type'] = forms.ChoiceField(
        choices=ORGANIZATIONSUBTYPES,
        initial="",
        label="Organization Sub Type",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "orginization_sub_type",
            }
        ),)

        AGENTSCLASSES = (("0", "--Select--"),)
        agents_classes = Levels.objects.filter(level_key = 'financing-agent-type', level_parent = 0).order_by("level_id") 
        for item in agents_classes:
                    AGENTSCLASSES= AGENTSCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['financial_agent_class'] = forms.ChoiceField(
        choices=AGENTSCLASSES,
        initial="",
        label="Financing Agency Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-financial-status-classification",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        AGENTSSUBCLASSES = (("0", "NONE"),)
        agents_sub_classes = Levels.objects.filter(level_key = 'financing-agent-type').order_by("level_id") 
        for item in agents_sub_classes:
                    AGENTSSUBCLASSES= AGENTSSUBCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
        self.fields['financial_agent_sub_class'] = forms.ChoiceField(
        choices=AGENTSSUBCLASSES,
        initial="",
        label="Financing Agency Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-status-class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        SCHEMESCLASSES = (("0", "--Select--"),)
        schemes_classes = Levels.objects.filter(level_key = 'financing-scheme-type', level_parent = 0).order_by("level_id")
        for item in schemes_classes: 
                    SCHEMESCLASSES = SCHEMESCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 
                    
        self.fields['financial_schemes_class'] = forms.ChoiceField(
        choices=SCHEMESCLASSES,
        initial="",
        label="Financing Schemes Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "financial_schemes_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        SCHEMESSUBCLASSES = (("0", "NONE"),)
        schemes_sub_classes = Levels.objects.filter(level_key = 'financing-scheme-type').order_by("level_id")
        for item in schemes_sub_classes: 
                    SCHEMESSUBCLASSES = SCHEMESSUBCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['financial_schemes_sub_class'] = forms.ChoiceField(
        choices=SCHEMESSUBCLASSES,
        initial="",
        label="Financing Schemes Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "financial_schemes_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        HEALTHCARESCLASSES = (("0", "--Select--"),)
        healthcare_classes = Levels.objects.filter(level_key = 'health-provider-type', level_parent = 0).order_by("level_id")
        for item in healthcare_classes:
                    HEALTHCARESCLASSES= HEALTHCARESCLASSES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
        self.fields['healthcare_class'] = forms.ChoiceField(
        choices=HEALTHCARESCLASSES,
        initial="",
        label="Healthcare Provider Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "healthcare_sources_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        HEALTHCARESSUBCLASSES = (("0", "NONE"),)
        healthcare_sub_classes = Levels.objects.filter(level_key = 'health-provider-type').order_by("level_id")
        for item in healthcare_sub_classes:
                    HEALTHCARESSUBCLASSES= HEALTHCARESSUBCLASSES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['healthcare_sub_class'] = forms.ChoiceField(
        choices=HEALTHCARESSUBCLASSES,
        initial="",
        label="healthcare Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "healthcare_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        FUNDINGS= (("0", "--Select--"),) 
        fundings = Levels.objects.filter(level_key = 'fundings', level_parent = 0).order_by("level_id")
        for item in fundings:
                    FUNDINGS = FUNDINGS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['funding_class'] = forms.ChoiceField(
        choices=FUNDINGS,
        initial="",
        label="Funding Source Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "funding_sources_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

        SUBFUNDINGS= (("0", "NONE"),) 
        sub_fundings = Levels.objects.filter(level_key = 'fundings').order_by("level_id")
        for item in sub_fundings:
                    SUBFUNDINGS = SUBFUNDINGS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['funding_sub_class'] = forms.ChoiceField(
        choices=SUBFUNDINGS,
        initial="",
        label="Funding Source Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "funding_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)

    class Meta:
        model = Organizations
        fields = (
            "name",
            "email",
            "type",
            "sub_type",
            "phone_number",
            "category",
            "financial_agent_class",
            "financial_agent_sub_class",
            "financial_schemes_name",
            "financial_schemes_class",
            "financial_schemes_sub_class",
            "healthcare_class",
            "healthcare_sub_class",
        )

