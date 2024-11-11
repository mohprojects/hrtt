import ast
from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from app.models.activities_inputs import Activities_Inputs
from app.models.levels import Levels
from app.models.organizations import Organizations
from app.models.implementers import Implementers
from app.models.fundings import Fundings
from app.models.projects import Projects
from app.utils import Utils


class ActivitiesInputsSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(ActivitiesInputsSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Activities_Inputs
        fields = ()

class ActivitiesInputsCreateForm(forms.ModelForm):

    input_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Input Class",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_class",
            }
        ),
    )

    input_sub_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Input Sub Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_sub_class",
            }
        ),
    )

    scheme_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Financing Schemes Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_scheme",
            }
        ),
    )

    scheme_sub_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Financing Schemes Sub Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_sub_scheme",
            }
        ),
    )

    funder = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Funder",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_funder",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
   
    transfer_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Funds transfer Class",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_transfer_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    sub_transfer_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Funds Transfer Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_transfer_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    implementer = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Implementer",
        required=True,
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_implementer",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    division = forms.CharField(
        label="Division/Department",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),
    )

    budget=forms.CharField(
        label="Budget",
        initial = '0.0',
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),
    )
    budget_currency =forms.ChoiceField(
        choices= (("0", "--Select--"),),
        label="Budget Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_budget_currency",
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),
    )
 
    def clean_input_class(self):
        data = self.cleaned_data["input_class"]
        return data
    
    def clean_input_category(self):
        data = self.cleaned_data["input_sub_class"]
        return data

    def clean_scheme_class (self):
        data = self.cleaned_data["scheme_class"]
        return data

    def clean_scheme_sub_class (self):
        data = self.cleaned_data["scheme_sub_class"]
        return data
    
    def clean_funder(self):
        data = self.cleaned_data["funder"]
        return data
    
    def clean_transfer_class(self):
        data = self.cleaned_data["transfer_class"]
        return data
    
    def clean_sub_transfer_class(self):
        data = self.cleaned_data["sub_transfer_class"]
        return data
    
    def clean_implementer(self):
        data = self.cleaned_data["implementer"]
        return data
    
    def clean_division(self):
        data = self.cleaned_data["division"]
        return data
    
    def clean_budget(self):
        data = self.cleaned_data["budget"]
        return data

    def clean_budget_currency(self):
        data = self.cleaned_data["budget_currency"]
        return data


    def clean(self):
        cleaned_data = super(ActivitiesInputsCreateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        project_id = kwargs.pop("project_id")
        super(ActivitiesInputsCreateForm, self).__init__(*args, **kwargs)
        INPUTS= (("0", "--Select--"),) 
        inputs = Levels.objects.filter(level_key = 'inputs', level_parent = 0).order_by("level_id")
        for item in inputs:
                    INPUTS = INPUTS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['input_class'] = forms.ChoiceField(
        choices=INPUTS,
        initial="",
        label="Input Class",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_class",
            }
        ),)

        SUBINPUTS= (("0", "NONE"),) 
        subinputs = Levels.objects.filter(level_key = 'inputs').order_by("level_id")
        for item in subinputs:
                    SUBINPUTS = SUBINPUTS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['input_sub_class'] = forms.ChoiceField(
        choices=SUBINPUTS,
        initial="",
        label="Input Sub Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_sub_class",
            }
        ),)
                    
        
            
        SCHEMESCLASSES = (("0", "--Select--"),)
        schemes_classes = Levels.objects.filter(level_key = 'financing-scheme-type', level_parent = 0).order_by("level_id")
        for item in schemes_classes: 
                    SCHEMESCLASSES = SCHEMESCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)

        self.fields['scheme_class'] = forms.ChoiceField(
        choices=SCHEMESCLASSES,
        initial="",
        label="Financing Schemes Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_scheme",
            }
        ),)

        SCHEMESSUBCLASSES = (("0", "NONE"),)
        schemes_sub_classes = Levels.objects.filter(level_key = 'financing-scheme-type').order_by("level_id")
        for item in schemes_sub_classes: 
                    SCHEMESSUBCLASSES = SCHEMESSUBCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 
                    
        self.fields['scheme_sub_class'] = forms.ChoiceField(
        choices=SCHEMESSUBCLASSES,
        initial="",
        label="Financing Schemes Sub Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_sub_scheme",
            }
        ),)
        ORGANIZATIONS = (('', '--select--'),)
        funders = Fundings.objects.filter(project_id = project_id)
        filtered_organization_ids = funders.values_list('funder_id', flat=True)
        organizations = Organizations.objects.filter(organization_id__in=filtered_organization_ids)
        #organizations = Organizations.objects.all()
        for item in organizations:
                            ORGANIZATIONS = ORGANIZATIONS + \
                                ((item.organization_id, item.organization_name),)

        self.fields['funder'] = forms.ChoiceField(
        choices= ORGANIZATIONS,
        initial="",
        label="Funder",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_funder",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)
        IMPLEMENTERS_ = (('', '--select--'),)
        impl_ids = Projects.objects.get(project_id = project_id)
        filtered_implementers_ids = ast.literal_eval(impl_ids.project_implementer)
        for id in filtered_implementers_ids:
            if "_" in id:
                org_impl= id.split('_')
                if org_impl[0].strip(' ') == 'impl':
                    item = Implementers.objects.get(pk= int(org_impl[1]))
                    IMPLEMENTERS_=IMPLEMENTERS_ + \
                        (("impl_"+ str(item.implementer_id), item.implementer_name),)
            else:
               item= Organizations.objects.get(pk=int(id))
               IMPLEMENTERS_ = IMPLEMENTERS_ + \
                        ((item.organization_id, item.organization_name),)
            
        self.fields['implementer'] = forms.ChoiceField(
        choices= IMPLEMENTERS_,
        initial="",
        label="Implementer",
        required=True,
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_implementer",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)
        SOURCECLASSES = (("0", "--Select--"),)
        source_classes = Levels.objects.filter(level_key = 'financing-source-type', level_parent = 0).order_by("level_id")
        for item in source_classes: 
                    SOURCECLASSES = SOURCECLASSES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
    
        self.fields['transfer_class'] = forms.ChoiceField(
            choices=SOURCECLASSES,
            initial="",
            label="Funds transfer Class",
            required=True,
            validators=[],
            widget=forms.Select(
                attrs={
                    "id": "id_activity_input_transfer_class",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ),)
        
        SOURCESUBCLASSES = (("0", "NONE"),)
        source_sub_classes = Levels.objects.filter(level_key = 'financing-source-type').order_by("level_id")
        for item in source_sub_classes: 
                    SOURCESUBCLASSES = SOURCESUBCLASSES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
        self.fields['sub_transfer_class'] = forms.ChoiceField(
            choices=SOURCESUBCLASSES,
            initial="",
            label="Funds Transfer Sub Class",
            required=False,
            validators=[],
            widget=forms.Select(
                attrs={
                    "id": "id_activity_input_transfer_sub_class",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ),
        )

        CURRENCIES = (("RWF", "RWF"),) 
        currencies = Levels.objects.filter(level_key = 'currency', level_parent = 0).order_by("level_id")
        for item in currencies:
                    CURRENCIES = CURRENCIES + \
                        ((str(item.level_name), str(item.level_name)),)

        self.fields['budget_currency'] =forms.ChoiceField(
        choices= CURRENCIES,
        label="Budget Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_budget_currency",
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),)
    class Meta:
        model = Activities_Inputs
        fields = (
            "input_class",
            "input_sub_class",
            "scheme_class",
            "scheme_sub_class",
            "funder",
            "transfer_class",
            "sub_transfer_class",
            "implementer",
            "division",
            "budget",
            "budget_currency",
        )


class ActivitiesInputsUpdateForm(forms.ModelForm):

    input_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Input Class",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_class",
            }
        ),
    )

    input_sub_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Input Sub Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_sub_class",
            }
        ),
    )

    scheme_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Financing SchemesClass",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_scheme",
            }
        ),
    )

    scheme_sub_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Financing Schemes Sub Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_sub_scheme",
            }
        ),
    )

    funder = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Funder",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_funder",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
   
    transfer_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Funds transfer Class",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_transfer_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    sub_transfer_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Funds Transfer Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_transfer_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    implementer = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Implementer",
        required=True,
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_implementer",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    division = forms.CharField(
        label="Division/Department",
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

    budget=forms.CharField(
        label="Budget",
        initial = '0.0',
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    budget_currency =forms.ChoiceField(
        choices= (("0", "--Select--"),),
        label="Budget Currency",
        required=True,
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_budget_currency",
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),
    )

    
    def clean_input_class(self):
        data = self.cleaned_data["input_class"]
        return data
    
    def clean_input_category(self):
        data = self.cleaned_data["input_sub_class"]
        return data

    def clean_scheme_class (self):
        data = self.cleaned_data["scheme_class"]
        return data

    def clean_scheme_sub_class (self):
        data = self.cleaned_data["scheme_sub_class"]
        return data
    
    def clean_funder(self):
        data = self.cleaned_data["funder"]
        return data
    
    def clean_transfer_class(self):
        data = self.cleaned_data["transfer_class"]
        return data
    
    def clean_sub_transfer_class(self):
        data = self.cleaned_data["sub_transfer_class"]
        return data
    
    def clean_implementer(self):
        data = self.cleaned_data["implementer"]
        return data
    
    def clean_division(self):
        data = self.cleaned_data["division"]
        return data
    
    def clean_budget(self):
        data = self.cleaned_data["budget"]
        return data

    def clean_budget_currency(self):
        data = self.cleaned_data["budget_currency"]
        return data

    def clean(self):
        cleaned_data = super(ActivitiesInputsUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        project_id = kwargs.pop("project_id")
        super(ActivitiesInputsUpdateForm, self).__init__(*args, **kwargs)
        INPUTS= (("0", "--Select--"),) 
        inputs = Levels.objects.filter(level_key = 'inputs', level_parent = 0).order_by("level_id")
        for item in inputs:
                    INPUTS = INPUTS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['input_class'] = forms.ChoiceField(
        choices=INPUTS,
        initial="",
        label="Input Class",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_class",
            }
        ),)

        SUBINPUTS= (("0", "NONE"),) 
        subinputs = Levels.objects.filter(level_key = 'inputs').order_by("level_id")
        for item in subinputs:
                    SUBINPUTS = SUBINPUTS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['input_sub_class'] = forms.ChoiceField(
        choices=SUBINPUTS,
        initial="",
        label="Input Sub Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_sub_class",
            }
        ),)
                    
        
            
        SCHEMESCLASSES = (("0", "--Select--"),)
        schemes_classes = Levels.objects.filter(level_key = 'financing-scheme-type', level_parent = 0).order_by("level_id")
        for item in schemes_classes: 
                    SCHEMESCLASSES = SCHEMESCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)

        self.fields['scheme_class'] = forms.ChoiceField(
        choices=SCHEMESCLASSES,
        initial="",
        label="Financing Schemes Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_scheme",
            }
        ),)

        SCHEMESSUBCLASSES = (("0", "NONE"),)
        schemes_sub_classes = Levels.objects.filter(level_key = 'financing-scheme-type').order_by("level_id")
        for item in schemes_sub_classes: 
                    SCHEMESSUBCLASSES = SCHEMESSUBCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 
                    
        self.fields['scheme_sub_class'] = forms.ChoiceField(
        choices=SCHEMESSUBCLASSES,
        initial="",
        label="Financing Schemes Sub Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_sub_scheme",
            }
        ),)
        ORGANIZATIONS = (('', '--select--'),)
        funders = Fundings.objects.filter(project_id = project_id)
        funders = Fundings.objects.filter(project_id = project_id)
        filtered_organization_ids = funders.values_list('funder_id', flat=True)
        organizations = Organizations.objects.filter(organization_id__in=filtered_organization_ids)
        #organizations = Organizations.objects.all()
        for item in organizations:
                            ORGANIZATIONS = ORGANIZATIONS + \
                                ((item.organization_id, item.organization_name),)

        self.fields['funder'] = forms.ChoiceField(
        choices= ORGANIZATIONS,
        initial="",
        label="Funder",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_funder",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)
        IMPLEMENTERS_ = (('', '--select--'),)
        impl_ids = Projects.objects.get(project_id = project_id)
        filtered_implementers_ids = ast.literal_eval(impl_ids.project_implementer)
        for id in filtered_implementers_ids:
            if "_" in id:
                org_impl= id.split('_')
                if org_impl[0].strip(' ') == 'impl':
                    item = Implementers.objects.get(pk= int(org_impl[1]))
                    IMPLEMENTERS_=IMPLEMENTERS_ + \
                        (("impl_"+ str(item.implementer_id), item.implementer_name),)
            else:
               item= Organizations.objects.get(pk=int(id))
               IMPLEMENTERS_ = IMPLEMENTERS_ + \
                        ((item.organization_id, item.organization_name),)
            
        self.fields['implementer'] = forms.ChoiceField(
        choices= IMPLEMENTERS_,
        initial="",
        label="Implementer",
        required=True,
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_implementer",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)
        SOURCECLASSES = (("0", "--Select--"),)
        source_classes = Levels.objects.filter(level_key = 'financing-source-type', level_parent = 0).order_by("level_id")
        for item in source_classes: 
                    SOURCECLASSES = SOURCECLASSES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
    
        self.fields['transfer_class'] = forms.ChoiceField(
            choices=SOURCECLASSES,
            initial="",
            label="Funds transfer Class",
            required=True,
            validators=[],
            widget=forms.Select(
                attrs={
                    "id": "id_activity_input_transfer_class",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ),)
        
        SOURCESUBCLASSES = (("0", "NONE"),)
        source_sub_classes = Levels.objects.filter(level_key = 'financing-source-type').order_by("level_id")
        for item in source_sub_classes: 
                    SOURCESUBCLASSES = SOURCESUBCLASSES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
        self.fields['sub_transfer_class'] = forms.ChoiceField(
            choices=SOURCESUBCLASSES,
            initial="",
            label="Funds Transfer Sub Class",
            required=False,
            validators=[],
            widget=forms.Select(
                attrs={
                    "id": "id_activity_input_transfer_sub_class",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ),
        )

        CURRENCIES = (("RWF", "RWF"),) 
        currencies = Levels.objects.filter(level_key = 'currency', level_parent = 0).order_by("level_id")
        for item in currencies:
                    CURRENCIES = CURRENCIES + \
                        ((str(item.level_name), str(item.level_name)),)

        self.fields['budget_currency'] =forms.ChoiceField(
        choices= CURRENCIES,
        label="Budget Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_budget_currency",
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),)
        
    class Meta:
        model = Activities_Inputs
        fields = (
            "input_class",
            "input_sub_class",
            "scheme_class",
            "scheme_sub_class",
            "funder",
            "transfer_class",
            "sub_transfer_class",
            "implementer",
            "division",
            "budget",
            "budget_currency",
            # "expenses",
            # "expenses_currency",
        )


class ActivitiesInputsViewForm(forms.ModelForm):

    input_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Input Class",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "id": "id_activity_input_class",
            }
        ),
    )

    input_sub_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Input Sub Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_sub_class",
            }
        ),
    )

    scheme_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Financing Schemes Class",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_scheme",
            }
        ),
    )

    scheme_sub_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Financing Schemes Sub Class",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_sub_scheme",
            }
        ),
    )

    funder = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Funder",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_funder",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
   
    transfer_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Funds transfer Class",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_transfer_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    sub_transfer_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Funds Transfer Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_transfer_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    implementer = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Implementer",
        required=True,
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_implementer",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    division = forms.CharField(
        label="Division/Department",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),
    )

    budget=forms.CharField(
        label="Budget",
        initial = '0.0',
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),
    )
    budget_currency =forms.ChoiceField(
        choices= (("0", "--Select--"),),
        label="Budget Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_budget_currency"
            }
        ),
    )

    expenses = forms.CharField(
        label="Expenditure ",
        initial = '0.0',
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),
    )

    expenses_currency = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        label="Expenditure Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),
    )
    
    def clean_input_class(self):
        data = self.cleaned_data["input_class"]
        return data
    
    def clean_input_category(self):
        data = self.cleaned_data["input_sub_class"]
        return data

    def clean_scheme_class (self):
        data = self.cleaned_data["scheme_class"]
        return data

    def clean_scheme_sub_class (self):
        data = self.cleaned_data["scheme_sub_class"]
        return data
    
    def clean_funder(self):
        data = self.cleaned_data["funder"]
        return data
    
    def clean_transfer_class(self):
        data = self.cleaned_data["transfer_class"]
        return data
    
    def clean_sub_transfer_class(self):
        data = self.cleaned_data["sub_transfer_class"]
        return data
    
    def clean_implementer(self):
        data = self.cleaned_data["implementer"]
        return data
    
    def clean_division(self):
        data = self.cleaned_data["division"]
        return data
    
    def clean_budget(self):
        data = self.cleaned_data["budget"]
        return data

    def clean_budget_currency(self):
        data = self.cleaned_data["budget_currency"]
        return data
    
    
    def clean_expenses(self):
        data = self.cleaned_data["expenses"]
        return data
    
    def clean_expenses_currency(self):
        data = self.cleaned_data["expenses_currency"]
        return data
    
    def clean(self):
        cleaned_data = super(ActivitiesInputsViewForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        project_id = kwargs.pop("project_id")
        super(ActivitiesInputsViewForm, self).__init__(*args, **kwargs)

        INPUTS= (("0", "--Select--"),) 
        inputs = Levels.objects.filter(level_key = 'inputs', level_parent = 0).order_by("level_id")
        for item in inputs:
                    INPUTS = INPUTS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['input_class'] = forms.ChoiceField(
        choices=INPUTS,
        initial="",
        label="Input Class",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_class",
            }
        ),)

        SUBINPUTS= (("0", "NONE"),) 
        subinputs = Levels.objects.filter(level_key = 'inputs').order_by("level_id")
        for item in subinputs:
                    SUBINPUTS = SUBINPUTS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['input_sub_class'] = forms.ChoiceField(
        choices=SUBINPUTS,
        initial="",
        label="Input Sub Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_sub_class",
            }
        ),)
                    
        
            
        SCHEMESCLASSES = (("0", "--Select--"),)
        schemes_classes = Levels.objects.filter(level_key = 'financing-scheme-type', level_parent = 0).order_by("level_id")
        for item in schemes_classes: 
                    SCHEMESCLASSES = SCHEMESCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)

        self.fields['scheme_class'] = forms.ChoiceField(
        choices=SCHEMESCLASSES,
        initial="",
        label="Financing Schemes Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_scheme",
            }
        ),)

        SCHEMESSUBCLASSES = (("0", "NONE"),)
        schemes_sub_classes = Levels.objects.filter(level_key = 'financing-scheme-type').order_by("level_id")
        for item in schemes_sub_classes: 
                    SCHEMESSUBCLASSES = SCHEMESSUBCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 
                    
        self.fields['scheme_sub_class'] = forms.ChoiceField(
        choices=SCHEMESSUBCLASSES,
        initial="",
        label="Financing Schemes Sub Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_sub_scheme",
            }
        ),)
        ORGANIZATIONS = (('', '--select--'),)
        funders = Fundings.objects.filter(project_id = project_id)
        filtered_organization_ids = funders.values_list('funder_id', flat=True)
        organizations = Organizations.objects.filter(organization_id__in=filtered_organization_ids)
        #organizations = Organizations.objects.all()
        for item in organizations:
                            ORGANIZATIONS = ORGANIZATIONS + \
                                ((item.organization_id, item.organization_name),)

        self.fields['funder'] = forms.ChoiceField(
        choices= ORGANIZATIONS,
        initial="",
        label="Funder",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_funder",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)
        IMPLEMENTERS_ = (('', '--select--'),)
        impl_ids = Projects.objects.get(project_id = project_id)
        filtered_implementers_ids = ast.literal_eval(impl_ids.project_implementer)
        for id in filtered_implementers_ids:
            if "_" in id:
                org_impl= id.split('_')
                if org_impl[0].strip(' ') == 'impl':
                    item = Implementers.objects.get(pk= int(org_impl[1]))
                    IMPLEMENTERS_=IMPLEMENTERS_ + \
                        (("impl_"+ str(item.implementer_id), item.implementer_name),)
            else:
               item= Organizations.objects.get(pk=int(id))
               IMPLEMENTERS_ = IMPLEMENTERS_ + \
                        ((item.organization_id, item.organization_name),)
            
        self.fields['implementer'] = forms.ChoiceField(
        choices= IMPLEMENTERS_,
        initial="",
        label="Implementer",
        required=True,
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_implementer",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)
        
        SOURCECLASSES = (("0", "--Select--"),)
        source_classes = Levels.objects.filter(level_key = 'financing-source-type', level_parent = 0).order_by("level_id")
        for item in source_classes: 
                    SOURCECLASSES = SOURCECLASSES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
    
        self.fields['transfer_class'] = forms.ChoiceField(
            choices=SOURCECLASSES,
            initial="",
            label="Funds transfer Class",
            required=True,
            validators=[],
            widget=forms.Select(
                attrs={
                    "id": "id_activity_input_transfer_class",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ),)
        
        SOURCESUBCLASSES = (("0", "NONE"),)
        source_sub_classes = Levels.objects.filter(level_key = 'financing-source-type').order_by("level_id")
        for item in source_sub_classes: 
                    SOURCESUBCLASSES = SOURCESUBCLASSES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
        self.fields['sub_transfer_class'] = forms.ChoiceField(
            choices=SOURCESUBCLASSES,
            initial="",
            label="Funds Transfer Sub Class",
            required=False,
            validators=[],
            widget=forms.Select(
                attrs={
                    "id": "id_activity_input_transfer_sub_class",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ),
        )

        CURRENCIES = (("RWF", "RWF"),) 
        currencies = Levels.objects.filter(level_key = 'currency', level_parent = 0).order_by("level_id")
        for item in currencies:
                    CURRENCIES = CURRENCIES + \
                        ((str(item.level_name), str(item.level_name)),)

        self.fields['budget_currency'] =forms.ChoiceField(
        choices= CURRENCIES,
        label="Budget Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_budget_currency",
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),)

        self.fields['expenses_currency'] = forms.ChoiceField(
        choices= CURRENCIES,
        label="Expenditure Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),)

    class Meta:
        model = Activities_Inputs
        fields = (
            "input_class",
            "input_sub_class",
            "scheme_class",
            "scheme_sub_class",
            "funder",
            "transfer_class",
            "sub_transfer_class",
            "implementer",
            "division",
            "budget",
            "budget_currency",
            "expenses",
            "expenses_currency",
        )

class ActivitiesInputsExpenditureForm(forms.ModelForm):

    input_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Input Class",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "readonly": True,
                # "disabled": True,
                "id": "id_activity_input_class",
            }
        ),
    )

    input_sub_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Input Sub Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "readonly": True,
                # "disabled": True,
                "id": "id_activity_input_sub_class",
            }
        ),
    )

    scheme_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Financing SchemesClass",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "readonly": True,
                # "disabled": True,
                "id": "id_activity_input_scheme",
            }
        ),
    )

    scheme_sub_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Financing Schemes Sub Class",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "readonly": True,
                # "disabled": True,
                "id": "id_activity_input_sub_scheme",
            }
        ),
    )

    funder = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Funder",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_funder",
                "class": "form-control",
                "style": "width:100%;",
                "readonly": True,
                # "disabled": True,
                "placeholder": "",
            }
        ),
    )
   
    transfer_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Funds transfer Class",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_transfer_class",
                "class": "form-control",
                "style": "width:100%;",
                "readonly": True,
                # "disabled": True,
                "placeholder": "",
            }
        ),
    )
    sub_transfer_class = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Funds Transfer Sub Class",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_transfer_sub_class",
                "class": "form-control",
                "style": "width:100%;",
                "readonly": True,
                # "disabled": True,
                "placeholder": "",
            }
        ),
    )

    implementer = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        initial="",
        label="Implementer",
        required=True,
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_implementer",
                "class": "form-control",
                "style": "width:100%;",
                "readonly": True,
                # "disabled": True,
                "placeholder": "",
            }
        ),
    )
    division = forms.CharField(
        label="Division/Department",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "readonly": True,
                # "disabled": True,
            }
        ),
    )

    budget=forms.CharField(
        label="Budget",
        initial = '0.0',
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                # "disabled": True,
            }
        ),
    )
    budget_currency =forms.ChoiceField(
        choices= (("0", "--Select--"),),
        label="Budget Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "readonly": True,
                # "disabled": True,
                "id": "id_activity_input_budget_currency"
            }
        ),
    )

    expenses = forms.CharField(
        label="Expenditure ",
        initial = '0.0',
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),
    )

    expenses_currency = forms.ChoiceField(
        choices= (("0", "--Select--"),),
        label="Expenditure Currency",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_expenses_currency"
            }
        ),
    )
    
    def clean_input_class(self):
        data = self.cleaned_data["input_class"]
        return data
    
    def clean_input_category(self):
        data = self.cleaned_data["input_sub_class"]
        return data

    def clean_scheme_class (self):
        data = self.cleaned_data["scheme_class"]
        return data

    def clean_scheme_sub_class (self):
        data = self.cleaned_data["scheme_sub_class"]
        return data
    
    def clean_funder(self):
        data = self.cleaned_data["funder"]
        return data
    
    def clean_transfer_class(self):
        data = self.cleaned_data["transfer_class"]
        return data
    
    def clean_sub_transfer_class(self):
        data = self.cleaned_data["sub_transfer_class"]
        return data
    
    def clean_implementer(self):
        data = self.cleaned_data["implementer"]
        return data
    
    def clean_division(self):
        data = self.cleaned_data["division"]
        return data
    
    def clean_budget(self):
        data = self.cleaned_data["budget"]
        return data

    def clean_budget_currency(self):
        data = self.cleaned_data["budget_currency"]
        return data
    
    
    def clean_expenses(self):
        data = self.cleaned_data["expenses"]
        return data
    
    def clean_expenses_currency(self):
        data = self.cleaned_data["expenses_currency"]
        return data

    def clean(self):
        cleaned_data = super(ActivitiesInputsExpenditureForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(ActivitiesInputsExpenditureForm, self).__init__(*args, **kwargs)

        INPUTS= (("0", "--Select--"),) 
        inputs = Levels.objects.filter(level_key = 'inputs', level_parent = 0).order_by("level_id")
        for item in inputs:
                    INPUTS = INPUTS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['input_class'] = forms.ChoiceField(
        choices=INPUTS,
        initial="",
        label="Input Class",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_class",
            }
        ),)

        SUBINPUTS= (("0", "NONE"),) 
        subinputs = Levels.objects.filter(level_key = 'inputs').order_by("level_id")
        for item in subinputs:
                    SUBINPUTS = SUBINPUTS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['input_sub_class'] = forms.ChoiceField(
        choices=SUBINPUTS,
        initial="",
        label="Input Sub Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_sub_class",
            }
        ),)
                    
        
            
        SCHEMESCLASSES = (("0", "--Select--"),)
        schemes_classes = Levels.objects.filter(level_key = 'financing-scheme-type', level_parent = 0).order_by("level_id")
        for item in schemes_classes: 
                    SCHEMESCLASSES = SCHEMESCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)

        self.fields['scheme_class'] = forms.ChoiceField(
        choices=SCHEMESCLASSES,
        initial="",
        label="Financing Schemes Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_scheme",
            }
        ),)

        SCHEMESSUBCLASSES = (("0", "NONE"),)
        schemes_sub_classes = Levels.objects.filter(level_key = 'financing-scheme-type').order_by("level_id")
        for item in schemes_sub_classes: 
                    SCHEMESSUBCLASSES = SCHEMESSUBCLASSES+ \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),) 
                    
        self.fields['scheme_sub_class'] = forms.ChoiceField(
        choices=SCHEMESSUBCLASSES,
        initial="",
        label="Financing Schemes Sub Class",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_input_sub_scheme",
            }
        ),)
        ORGANIZATIONS = (('', '--select--'),)
        organizations = Organizations.objects.all()
        for item in organizations:
                            ORGANIZATIONS = ORGANIZATIONS + \
                                ((item.organization_id, item.organization_name),)

        self.fields['funder'] = forms.ChoiceField(
        choices= ORGANIZATIONS,
        initial="",
        label="Funder",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_funder",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)
        IMPLEMENTERS_ = (('', '--select--'),)
        organizations_ = Organizations.objects.all()
        for item in organizations_:
             IMPLEMENTERS_ = IMPLEMENTERS_ + \
                    ((item.organization_id, item.organization_name),)
        implementers = Implementers.objects.all()
        for item in implementers:
            IMPLEMENTERS_=IMPLEMENTERS_ + \
                    (("impl_"+ str(item.implementer_id), item.implementer_name),)

        self.fields['implementer'] = forms.ChoiceField(
        choices= IMPLEMENTERS_,
        initial="",
        label="Implementer",
        required=True,
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_implementer",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)
        SOURCECLASSES = (("0", "--Select--"),)
        source_classes = Levels.objects.filter(level_key = 'financing-source-type', level_parent = 0).order_by("level_id")
        for item in source_classes: 
                    SOURCECLASSES = SOURCECLASSES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
    
        self.fields['transfer_class'] = forms.ChoiceField(
            choices=SOURCECLASSES,
            initial="",
            label="Funds transfer Class",
            required=True,
            validators=[],
            widget=forms.Select(
                attrs={
                    "id": "id_activity_input_transfer_class",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ),)
        
        SOURCESUBCLASSES = (("0", "NONE"),)
        source_sub_classes = Levels.objects.filter(level_key = 'financing-source-type').order_by("level_id")
        for item in source_sub_classes: 
                    SOURCESUBCLASSES = SOURCESUBCLASSES + \
                        ((item.level_id, str(item.level_code) + ': ' + str(item.level_name)),)
        self.fields['sub_transfer_class'] = forms.ChoiceField(
            choices=SOURCESUBCLASSES,
            initial="",
            label="Funds Transfer Sub Class",
            required=False,
            validators=[],
            widget=forms.Select(
                attrs={
                    "id": "id_activity_input_transfer_sub_class",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ),
        )

        CURRENCIES = (("RWF", "RWF"),) 
        currencies = Levels.objects.filter(level_key = 'currency', level_parent = 0).order_by("level_id")
        for item in currencies:
                    CURRENCIES = CURRENCIES + \
                        ((str(item.level_name), str(item.level_name)),)

        self.fields['budget_currency'] =forms.ChoiceField(
        choices= CURRENCIES,
        label="Budget Currency",
        required=False,
        widget=forms.Select(
            attrs={
                "id": "id_activity_input_budget_currency",
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),)

        self.fields['expenses_currency'] = forms.ChoiceField(
        choices= CURRENCIES,
        label="Expenditure Currency",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),)
        
    class Meta:
        model = Activities_Inputs
        fields = (
            "input_class",
            "input_sub_class",
            "scheme_class",
            "scheme_sub_class",
            "funder",
            "transfer_class",
            "sub_transfer_class",
            "implementer",
            "division",
            "budget",
            "budget_currency",
            "expenses",
            "expenses_currency",
        )


